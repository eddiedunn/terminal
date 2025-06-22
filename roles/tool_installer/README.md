# Ansible Role: tool_installer

This role is part of the `your_namespace.terminal` collection and is now the **single source of truth for userland CLI tool installation**.

## Responsibilities
- Defines all tool metadata in `defaults/main.yml` (`tool_installer_definitions`).
- Stores completions metadata in `files/completions_metadata.yml`.
- Stages all binaries and completions in `files/` using the canonical `download_helper.py` script.
- Installs binaries to `~/.local/bin`, completions to the appropriate directories, and shell init snippets to `~/.config/shell_init.d/`.

## How It Works
1. **Define Tools:** Add or update tool entries in `defaults/main.yml` under `tool_installer_definitions`.
2. **Define Completions:** Add or update completions in `files/completions_metadata.yml`.
3. **Stage Artifacts:** Run `python3 roles/tool_installer/scripts/download_helper.py roles/tool_installer` to download and stage all needed files.
4. **Install:** Run the role in your playbook, specifying tools via `tool_installer_tools`.

## Reference
- See `BINARY_MANAGEMENT.md` and `CROSS_PLATFORM_BINARY_DISCUSSION.md` for the authoritative design and data model for binaries and completions.

This role replaces all previous tool installation logic from `user_setup` and should be the only location for tool and completion management logic.
