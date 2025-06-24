# Terminal Tool Installer: Binary & Completion Management

This document describes the authoritative workflow for managing userland CLI tool binaries and completions in the `tool_installer` role. It reflects the actual code and artifact cache workflow implemented in the Ansible collection.

## Data Model
- **Tool Definitions:** All tool metadata is defined in `defaults/main.yml` under `terminal_setup_tools_defaults` (or `tool_installer_definitions`).
- **Completions:** All completions metadata is in `files/completions_metadata.yml`.

## Artifact Cache Workflow
- The controller (not the remote host) maintains an artifact cache at `/tmp/terminal-ansible-artifacts` (configurable).
- Binaries are staged here, separated by OS and architecture, e.g.:
  - `/tmp/terminal-ansible-artifacts/darwin/x86_64/ripgrep/14.1.0/ripgrep-14.1.0`
  - `/tmp/terminal-ansible-artifacts/linux/x86_64/ripgrep/14.1.0/ripgrep-14.1.0`
- The artifact cache is never committed to the repository, preventing repo pollution.

## Download & Staging
- Use `scripts/download_helper.py` to fetch and stage all binaries into the artifact cache on the controller.
- For each tool with `install_type: binary` and a matching OS/arch:
  - Downloads the archive from the specified URL.
  - Verifies (or computes) the checksum.
  - Extracts the binary (e.g., `rg` for ripgrep) and renames it to the canonical format (`ripgrep-<version>`).
  - Stages it in the artifact cache.
- Updates a checksums cache file for reproducibility.

## Playbook Pre-Flight Check
- Before running install roles, the playbook checks that all required binaries are present in the artifact cache for the target OS/arch.
- If any are missing, the playbook fails early with a clear message.

## Installation on Remote Host
- The playbook copies the required binaries from the artifact cache to the remote user's `~/.local/bin/` (or `terminal_setup_bin_dir`).
- This is done using Ansible's `copy` or `synchronize` modules.

## Symlink and PATH Management
- For tools like ripgrep, only the versioned binary is staged and copied.
- The role then ensures a symlink (e.g., `rg`) points to the versioned binary, so users can call `rg` as expected.
- No separate download or cache entry for the symlink name is needed.

## Offline/Airgapped Install Support
- Once the artifact cache is populated, remote hosts can be provisioned fully offline, with no internet access required.

## Reference
- For cross-platform and reproducibility design, see `CROSS_PLATFORM_BINARY_DISCUSSION.md` in this directory.

This document supersedes any previous binary management docs in other roles.
