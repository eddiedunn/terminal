# Ansible Role: tool_installer

This role is part of the `eddiedunn.terminal` collection and is the **single source of truth for userland CLI tool installation**.

## Responsibilities
- Defines all tool metadata in `defaults/main.yml` (`terminal_setup_tools_defaults` or `tool_installer_definitions`).
- Stores completions metadata in `files/completions_metadata.yml`.
- Stages all binaries in a controller-local artifact cache using the canonical `download_helper.py` script.
- Installs binaries to `~/.local/bin`, completions to the appropriate directories, and shell init snippets to `~/.config/shell_init.d/`.

## Artifact Cache & Binary Install Workflow

### 1. Tool Metadata Definition
- All tool metadata is defined in `defaults/main.yml` under `terminal_setup_tools_defaults`.
- Each tool entry specifies:
  - `name`, `version`, `install_type` (must be `binary` for binaries)
  - `binaries` section, mapping OS/arch to download URLs and archive details.

### 2. Controller-Local Artifact Cache
- The controller (not the remote host) maintains an artifact cache at `/tmp/terminal-ansible-artifacts` (configurable).
- Binaries are staged here, separated by OS and architecture, e.g.:
  - `/tmp/terminal-ansible-artifacts/darwin/x86_64/ripgrep/14.1.0/ripgrep-14.1.0`
  - `/tmp/terminal-ansible-artifacts/linux/x86_64/ripgrep/14.1.0/ripgrep-14.1.0`
- The artifact cache is never committed to the repository, preventing repo pollution.

### 3. Download Helper Script
- The playbook runs `roles/tool_installer/scripts/download_helper.py` on the controller.
- This script:
  - Reads tool definitions from `defaults/main.yml`.
  - For each tool with `install_type: binary` and a matching OS/arch:
    - Downloads the archive from the specified URL.
    - Verifies (or computes) the checksum.
    - Extracts the binary (e.g., `rg` for ripgrep) and renames it to the canonical format (`ripgrep-<version>`).
    - Stages it in the artifact cache.
  - Updates a checksums cache file for reproducibility.

### 4. Playbook Pre-Flight Check
- Before running install roles, the playbook checks that all required binaries are present in the artifact cache for the target OS/arch.
- If any are missing, the playbook fails early with a clear message.

### 5. Copy to Remote Host
- When installing on a remote host, the playbook copies the required binaries from the artifact cache to the remote user's `~/.local/bin/` (or `terminal_setup_bin_dir`).
- This is done using Ansible's `copy` or `synchronize` modules.

### 6. Symlink and PATH Management
- For tools like ripgrep, only the versioned binary is staged and copied.
- The role then ensures a symlink (e.g., `rg`) points to the versioned binary, so users can call `rg` as expected.
- No separate download or cache entry for the symlink name is needed.

### 7. Offline/Airgapped Install Support
- Once the artifact cache is populated, remote hosts can be provisioned fully offline, with no internet access required.

## Reference
- See `BINARY_MANAGEMENT.md` and `CROSS_PLATFORM_BINARY_DISCUSSION.md` for the authoritative design and data model for binaries and completions.

This role replaces all previous tool installation logic from `user_setup` and should be the only location for tool and completion management logic.
