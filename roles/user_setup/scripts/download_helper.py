#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ansible terminal_setup role binary download helper.

This script is designed to be called from an Ansible playbook on the controller.
It reads tool definitions from the role's defaults/main.yml, downloads the
necessary binaries, and places them in the role's files/ directory.

It automates checksum verification by:
1. Using a `checksum_url` if provided for a direct checksum file.
2. Parsing a release-wide checksum file (e.g., sha256sums.txt) if configured.
3. Calculating the SHA256 sum if no official one is available.

All fetched/calculated checksums are cached in `files/checksums.yml` to speed
up subsequent runs and enable offline operation.
"""

import argparse
import hashlib
import os
import re
import shutil
import ssl
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import yaml

# Disable SSL certificate verification for local requests if needed for proxies.
# Not recommended for production, but can be useful for development.
# ssl._create_default_https_context = ssl._create_unverified_context

class Downloader:
    """Handles the download and verification of binaries."""

    def __init__(self, role_path: Path):
        self.role_path = role_path
        self.files_dir = self.role_path / "files"
        self.defaults_file = self.role_path / "defaults" / "main.yml"
        self.checksums_file = self.files_dir / "checksums.yml"
        self.temp_dir = Path(tempfile.gettempdir())
        self.known_checksums = {}
        self.changed = False

    def run(self):
        """Main execution method."""
        print("Starting binary download process...")
        self.files_dir.mkdir(exist_ok=True)
        self._load_data()

        tools = self.defaults.get("terminal_setup_tools", None)
        if not tools:
            print("[DEBUG] 'terminal_setup_tools' not found in YAML. Falling back to 'terminal_setup_tools_defaults'.")
            tools = self.defaults.get("terminal_setup_tools_defaults", [])
        for tool in tools:
            if not isinstance(tool, dict):
                print(f"[SKIP] Non-dict entry in tools list: {repr(tool)} (type: {type(tool)})")
                continue
            if tool.get("install_type") != "binary":
                continue
            self._process_tool(tool)

        self.run_completions()

        self._write_checksums()
        if self.changed:
            # Output a string that Ansible can detect to mark the task as changed.
            print("CHANGED: Binaries were downloaded or checksums updated.")
        print("Binary download process finished.")

    def _load_data(self):
        """Loads YAML data from defaults and checksums cache."""
        with open(self.defaults_file, "r", encoding="utf-8") as f:
            self.defaults = yaml.safe_load(f)
        if self.checksums_file.exists():
            with open(self.checksums_file, "r", encoding="utf-8") as f:
                self.known_checksums = yaml.safe_load(f) or {}
        else:
            self.known_checksums = {}

    def _process_tool(self, tool):
        """Processes a single tool definition."""
        tool_name = tool["name"]
        version = str(tool["version"])
        print(f"\nProcessing tool: {tool_name} v{version}")

        for os_name, arches in tool.get("binaries", {}).items():
            for arch_name, details in arches.items():
                self._process_binary(tool, os_name, arch_name, details)

    def _process_binary(self, tool, os_name, arch_name, details):
        """Processes a single binary variant of a tool."""
        version = str(tool["version"])
        url = details["url"].format(version=version)
        archive_filename = url.split("/")[-1]
        
        executable_name = tool.get("executable_name", tool["name"])
        final_dir = self.files_dir / os_name.lower() / arch_name / tool["name"] / version
        versioned_executable = f"{executable_name}-{version}"
        print(f"[DEBUG] Processing: tool={tool['name']}, os={os_name}, arch={arch_name}, version={version}")
        print(f"[DEBUG] Intended directory: {final_dir}")
        print(f"[DEBUG] Intended binary path: {final_dir / versioned_executable}")
        if not final_dir.exists():
            print(f"[DEBUG] Directory {final_dir} does not exist. Creating...")
            final_dir.mkdir(parents=True, exist_ok=True)
            print(f"[DEBUG] Directory {final_dir} created.")
        else:
            print(f"[DEBUG] Directory {final_dir} already exists.")
        final_path = final_dir / versioned_executable
        
        if final_path.exists():
            print(f"  - SKIPPING {final_path} (already exists)")
            return

        checksum_key = f"{tool['name']}-{version}-{os_name}-{arch_name}"
        checksum_to_use = self.known_checksums.get(checksum_key)

        if not checksum_to_use:
            print(f"[DEBUG] No cached checksum for {checksum_key}. Determining checksum...")
            checksum_to_use = self._determine_checksum(tool, details, archive_filename, url)
            if checksum_to_use:
                print(f"[DEBUG] Checksum determined: {checksum_to_use}")
                self.known_checksums[checksum_key] = checksum_to_use
                self.changed = True
        else:
            print(f"  - Using cached checksum for {archive_filename}")

        # Download and verify
        print(f"[DEBUG] Downloading {url} to {archive_filename} with checksum {checksum_to_use}")
        archive_path = self._download_file(url, archive_filename, checksum_to_use)
        if not archive_path:
            print(f"[DEBUG] Download failed for {url}")
            return
        print(f"[DEBUG] Downloaded to {archive_path}")

        # Extract and copy
        print(f"  - Extracting {archive_filename}...")
        executable_in_archive = (details.get("executable_in_archive") or executable_name).format(version=version)
        print(f"[DEBUG] Extracting/copying from {archive_path} to {final_path} (executable in archive: {executable_in_archive})")
        self._extract_and_copy(archive_path, executable_in_archive, final_path)
        print(f"[DEBUG] Extraction/copy complete: {final_path}")
        # Do not delete the archive, leave it in place for completions extraction
#         print(f"[DEBUG] Removing archive: {archive_path}")
#         archive_path.unlink()

    def _determine_checksum(self, tool, details, archive_filename, url):
        """Finds the checksum from remote or calculates it."""
        version = str(tool["version"])
        
        # Strategy 1: Direct checksum URL
        if "checksum_url" in details:
            cs_url = details["checksum_url"].format(version=version)
            print(f"  - Fetching checksum from {cs_url}")
            content = self._fetch_url_content(cs_url)
            if content:
                # Assumes file contains 'checksum filename' or just 'checksum'
                return f"sha256:{content.split(' ')[0].strip()}"

        # Strategy 2: Release-wide checksums file
        checksum_info = tool.get("checksum_info", {})
        if "release_checksums_file" in checksum_info:
            release_file = checksum_info["release_checksums_file"].format(version=version)
            base_url = "/".join(url.split("/")[:-1])
            cs_url = f"{base_url}/{release_file}"
            print(f"  - Fetching and parsing release checksum file: {cs_url}")
            content = self._fetch_url_content(cs_url)
            if content:
                for line in content.splitlines():
                    if archive_filename in line:
                        return f"sha256:{line.split(' ')[0].strip()}"

        # Strategy 3: Calculate it ourselves
        print(f"  - No remote checksum found. Calculating for {archive_filename}.")
        archive_path = self._download_file(url, archive_filename)
        if not archive_path:
            return None
            
        sha256_hash = hashlib.sha256()
        with open(archive_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        # Clean up file used for calculation
        archive_path.unlink()
        
        return f"sha256:{sha256_hash.hexdigest()}"

    def _download_file(self, url, filename, checksum=None):
        """Downloads a file and optionally verifies its checksum."""
        dest_path = self.temp_dir / filename
        print(f"  - Downloading {url} to {dest_path}")
        try:
            urllib.request.urlretrieve(url, dest_path)
        except Exception as e:
            print(f"    ERROR: Failed to download {url}: {e}", file=sys.stderr)
            return None

        if checksum:
            print(f"    Verifying checksum ({checksum})...")
            sha256_hash = hashlib.sha256()
            with open(dest_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            if not checksum.endswith(sha256_hash.hexdigest()):
                print(f"    ERROR: Checksum mismatch for {filename}!", file=sys.stderr)
                print(f"      Expected: {checksum}", file=sys.stderr)
                print(f"      Got:      {sha256_hash.hexdigest()}", file=sys.stderr)
                dest_path.unlink()
                return None
            print("    Checksum OK.")
        return dest_path

    def _fetch_url_content(self, url):
        """Fetches the text content of a URL."""
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return response.read().decode("utf-8")
        except Exception as e:
            print(f"    WARNING: Could not fetch {url}: {e}", file=sys.stderr)
        return None

    def _extract_and_copy(self, archive_path, file_in_archive, final_path):
        """Extracts an executable from an archive and copies it to the final destination."""
        extract_dir = self.temp_dir / f"extract-{archive_path.stem}"
        extract_dir.mkdir(exist_ok=True)
        
        try:
            if archive_path.name.endswith((".tar.gz", ".tgz")):
                with tarfile.open(archive_path, "r:gz") as tar:
                    tar.extractall(path=extract_dir)
            elif archive_path.name.endswith(".zip"):
                with zipfile.ZipFile(archive_path, "r") as z:
                    z.extractall(path=extract_dir)
            else: # It's a raw binary
                shutil.copy(archive_path, extract_dir / file_in_archive)

            src_file = extract_dir / file_in_archive
            if not src_file.exists():
                # Fallback for nested directories
                for root, _, files in os.walk(extract_dir):
                    if os.path.basename(file_in_archive) in files:
                        src_file = Path(root) / os.path.basename(file_in_archive)
                        break

            if not src_file.exists():
                raise FileNotFoundError(f"Could not find '{file_in_archive}' in {archive_path}")

            shutil.copy(src_file, final_path)
            os.chmod(final_path, 0o755)
            print(f"  - Successfully placed executable at {final_path}")
            self.changed = True
        except Exception as e:
            print(f"    ERROR: Failed to extract {archive_path}: {e}", file=sys.stderr)
        finally:
            shutil.rmtree(extract_dir)

    def _find_staged_binary(self, tool_entry):
        """Return the path to the staged binary for a tool if it exists, else None."""
        import platform
        os_name = platform.system().lower()
        arch = platform.machine().lower()
        if arch in ("arm64", "aarch64"):
            arch = "aarch64"
        elif arch in ("x86_64", "amd64"):
            arch = "x86_64"
        version = tool_entry.get("version")
        tool_name = tool_entry.get("name")
        if not version or not tool_name:
            return None
        bin_path = self.files_dir / os_name / arch / tool_name / str(version) / f"{tool_name}-{version}"
        if bin_path.exists():
            return str(bin_path)
        return None

    def run_completions(self):
        """Process completions_metadata.yml and stage completions scripts."""
        completions_meta_file = self.files_dir / "completions_metadata.yml"
        completions_dir = self.files_dir / "completions"
        if not completions_meta_file.exists():
            print("[COMPLETIONS] No completions_metadata.yml found, skipping completions staging.")
            return
        with open(completions_meta_file, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        for entry in meta.get("completions", []):
            tool = entry.get("name")
            for shell in ("zsh", "bash", "fish"):
                shell_info_list = entry.get(shell)
                if not shell_info_list:
                    continue
                # Support both old dict and new list-of-dicts formats
                if not isinstance(shell_info_list, list):
                    shell_info_list = [shell_info_list]
                for shell_info in shell_info_list:
                    if not shell_info:
                        continue
                    method = shell_info.get("method")
                    output = shell_info.get("output")
                    if method == "cli":
                        cmd = shell_info.get("command")
                        if not cmd or not output:
                            continue
                        shell_dir = completions_dir / shell
                        shell_dir.mkdir(parents=True, exist_ok=True)
                        out_path = shell_dir / output
                        print(f"[COMPLETIONS][CLI] Running '{cmd}' for {tool} ({shell}), writing to {out_path}")
                        try:
                            import subprocess
                            import os
                            staged_bin = self._find_staged_binary(entry)
                            env = os.environ.copy()
                            if staged_bin:
                                env["PATH"] = f"{os.path.dirname(staged_bin)}:{env['PATH']}"
                                print(f"[COMPLETIONS][CLI] Using staged binary: {staged_bin}")
                            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
                            if tool == "zoxide" and shell == "zsh" and output == "zoxide.zsh":
                                content = result.stdout.decode("utf-8")
                                filtered = "\n".join(
                                    line for line in content.splitlines()
                                    if not (line.strip().startswith("eval ") or "zoxide init" in line)
                                )
                                with open(out_path, "w", encoding="utf-8") as outf:
                                    outf.write(filtered)
                            else:
                                with open(out_path, "wb") as outf:
                                    outf.write(result.stdout)
                            self.changed = True
                        except Exception as e:
                            print(f"[COMPLETIONS][ERROR] Failed to generate completion for {tool} ({shell}): {e}", file=sys.stderr)
                    elif method == "url":
                        url = shell_info.get("url")
                        if not url or not output:
                            continue
                        shell_dir = completions_dir / shell
                        shell_dir.mkdir(parents=True, exist_ok=True)
                        out_path = shell_dir / output
                        print(f"[COMPLETIONS][URL] Downloading {url} for {tool} ({shell}), saving to {out_path}")
                        try:
                            urllib.request.urlretrieve(url, out_path)
                            self.changed = True
                        except Exception as e:
                            print(f"[COMPLETIONS][ERROR] Failed to download completion for {tool} ({shell}): {e}", file=sys.stderr)
                    elif method == "archive":
                        import platform
                        os_name = platform.system().lower()
                        arch = platform.machine().lower()
                        if arch in ("arm64", "aarch64"):
                            arch = "aarch64"
                        elif arch in ("x86_64", "amd64"):
                            arch = "x86_64"
                        version = entry.get("version")
                        tool_name = entry.get("name")
                        tool_dir = self.files_dir / os_name / arch / tool_name / str(version)
                        if not tool_dir.exists():
                            print(f"[COMPLETIONS][ARCHIVE][ERROR] Tool dir not found: {tool_dir}", file=sys.stderr)
                            continue
                        archive_candidates = list(tool_dir.glob("*.zip")) + list(tool_dir.glob("*.tar.gz")) + list(tool_dir.glob("*.tgz"))
                        if not archive_candidates:
                            print(f"[COMPLETIONS][ARCHIVE][ERROR] No archive found for {tool} in {tool_dir}", file=sys.stderr)
                            continue
                        archive_path = archive_candidates[0]
                        file_in_archive = shell_info.get("archive_path")
                        if not file_in_archive or not output:
                            continue
                        shell_dir = completions_dir / shell
                        shell_dir.mkdir(parents=True, exist_ok=True)
                        out_path = shell_dir / output
                        print(f"[COMPLETIONS][ARCHIVE] Extracting {file_in_archive} from {archive_path} for {tool} ({shell}), writing to {out_path}")
                        try:
                            extracted = False
                            if archive_path.suffix == ".zip":
                                import zipfile
                                with zipfile.ZipFile(archive_path, "r") as z:
                                    if file_in_archive in z.namelist():
                                        with z.open(file_in_archive) as src, open(out_path, "wb") as dst:
                                            dst.write(src.read())
                                        extracted = True
                            elif archive_path.suffixes[-2:] == [".tar", ".gz"] or archive_path.suffix == ".tgz":
                                import tarfile
                                with tarfile.open(archive_path, "r:gz") as tar:
                                    try:
                                        member = tar.getmember(file_in_archive)
                                        with tar.extractfile(member) as src, open(out_path, "wb") as dst:
                                            dst.write(src.read())
                                        extracted = True
                                    except KeyError:
                                        print(f"[COMPLETIONS][ARCHIVE][ERROR] {file_in_archive} not found in {archive_path}", file=sys.stderr)
                            if extracted:
                                self.changed = True
                            else:
                                print(f"[COMPLETIONS][ARCHIVE][ERROR] Failed to extract {file_in_archive} from {archive_path}", file=sys.stderr)
                        except Exception as e:
                            print(f"[COMPLETIONS][ARCHIVE][ERROR] Exception extracting {file_in_archive} from {archive_path}: {e}", file=sys.stderr)
                    elif method in ("plugin", "none"):
                        # Nothing to do at download step
                        continue

    def _write_checksums(self):
        """Writes the updated checksum cache to disk if changes were made."""
        if self.changed:
            print("\nUpdating checksums cache file: files/checksums.yml")
            with open(self.checksums_file, "w", encoding="utf-8") as f:
                yaml.dump(self.known_checksums, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and manage binaries for the terminal_setup Ansible role."
    )
    parser.add_argument(
        "role_path",
        type=Path,
        help="The path to the 'terminal_setup' role directory.",
    )
    args = parser.parse_args()

    if not (args.role_path / "defaults" / "main.yml").exists():
        print(f"ERROR: Not a valid role path: {args.role_path}", file=sys.stderr)
        sys.exit(1)

    downloader = Downloader(args.role_path)
    downloader.run()
