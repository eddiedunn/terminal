# Ansible Role: tool_installer

This role is part of the `your_namespace.terminal` collection.

It is responsible for installing userland CLI tools from pre-downloaded binaries and deploying their corresponding shell completions and shell init snippets.

## How It Works

1. **Downloads (Controller-side):** Uses a helper script to fetch binaries and completions based on metadata and tool definitions.
2. **Installation (Target-side):**
    - Copies the correct binary for the target OS/architecture to `~/.local/bin/`.
    - Copies shell completion files to the appropriate user directory (`~/.bash_completion.d`, `~/.zsh/completions`, etc.).
    - For tools requiring shell initialization (e.g., `zoxide`, `starship`), it creates a script in `~/.config/shell_init.d/`.

## Role Variables

- `tool_installer_tools`: A list of tool names to install. Example: `['fzf', 'bat', 'eza']`.
- `tool_installer_definitions`: The master list of all tool definitions (usually not overridden by the user).
