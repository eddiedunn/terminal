# Terminal Tool Installer: Binary & Completion Management

This document consolidates the design and implementation details for managing userland CLI tool binaries and completions in the `tool_installer` role.

## Data Model
- **Tool Definitions:** All tool metadata is defined in `defaults/main.yml` under `tool_installer_definitions`.
- **Completions:** All completions metadata is in `files/completions_metadata.yml`.

## Staging
- Use `scripts/download_helper.py` to fetch and stage all binaries and completions into `files/`.

## Installation
- The role copies binaries from staged files to `~/.local/bin/` and completions to the appropriate shell completions directory.
- Shell init snippets are deployed to `~/.config/shell_init.d/` as needed.

## Reference
- For cross-platform and reproducibility design, see `CROSS_PLATFORM_BINARY_DISCUSSION.md` in this directory.

This document supersedes any previous binary management docs in other roles.
