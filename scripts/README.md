# Terminal Environment Scripts

This directory contains utility scripts for development, testing, and verification of the eddiedunn.terminal Ansible collection.

## reset_local_terminal_env.sh
Removes all files, directories, binaries, and configuration changes created by the local setup playbook. Use this to reset your shell environment before re-running or testing the playbook.

- Removes:
  - `~/.local/bin`, `~/.config/shell_init.d`, completions directories
  - Tool-specific directories (e.g., `~/.nvm`, `~/.pyenv`, `~/.cargo`, `~/.sdkman`, Go directories)
  - Shell init snippets for tools
  - Sourcing lines from `.bashrc`, `.zshrc`, `.profile`
  - The artifact cache at `/tmp/terminal-ansible-artifacts`

## verify_local_terminal_env.sh
Checks for the presence of key files, directories, binaries, and shell config changes expected after running the local setup playbook. Use this to confirm the playbook worked as intended.

- Checks:
  - Core and tool-specific directories, including SDKMAN and Go
  - Shell init snippets for all tools
  - Binaries on PATH
  - Artifact cache presence
  - Configuration files like `starship.toml` and `sheldon/plugins.toml`
  - Sourcing of shell_init.d in shell configs

---

**Usage:**

```sh
./reset_local_terminal_env.sh
# ...run your playbook...
./verify_local_terminal_env.sh
```

## reset_appuser_terminal_env.sh
Performs the same cleanup as `reset_local_terminal_env.sh` but targets the
`appuser` account. Useful when the playbook was executed as that user.

## verify_appuser_terminal_env.sh
Runs the verification checks against the `appuser` environment instead of the
current user.

*For development use only. These scripts are destructive and not intended for production systems.*
