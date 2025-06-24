# Ansible Role: system_dependencies


## Supported Platforms
- Debian/Ubuntu (via `apt`)
- macOS (via `homebrew`)

## Role Variables
- `system_dependencies_tools`: List of tool names to install dependencies for. Example: `[ 'nvm', 'pyenv', 'rustup' ]`

## Example Usage
```yaml
- hosts: all
  become: true
  roles:
    - role: system_dependencies
      vars:
        system_dependencies_tools:
          - nvm
          - pyenv
          - rustup
      vars:
        terminal_setup_profile_tools:
          - nvm
          - pyenv
          - rustup
```

## How It Works
- For each tool listed in `system_dependencies_tools`, the role will install the required system packages for the detected OS.
- No user-level configuration is performed by this role.

## Extending
If you need to support additional tools or platforms, edit `tasks/main.yml` and add the required package mappings.
