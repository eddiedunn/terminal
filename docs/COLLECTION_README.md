# eddiedunn.terminal Collection Overview

This collection assembles several roles to configure a reproducible terminal environment on Linux and macOS. The `profile` role is the main entry point and pulls in helper roles such as `tool_installer`, `system_dependencies`, `nvm`, `pyenv`, and `rustup` to install tools and set up shell integrations.

## Installation

Build and install from the collection root:

```bash
ansible-galaxy collection build --force
ansible-galaxy collection install ./eddiedunn-terminal-*.tar.gz --force -p ~/.ansible/collections
```

Alternatively, add `eddiedunn.terminal` to your `collections/requirements.yml` and run `ansible-galaxy collection install -r collections/requirements.yml`.

## Usage

Reference roles using their fully qualified collection name. Example:

```yaml
- hosts: all
  roles:
    - eddiedunn.terminal.profile
```

Role-specific documentation with variables and examples lives in each role's `README.md` under `roles/<role_name>/`. See `docs/BINARY_MANAGEMENT.md` and `docs/COMPLETIONS_WORKFLOW.md` for more details on binaries and completions.

