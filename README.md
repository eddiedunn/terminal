# O'Reilly Auto Terminal Collection

A comprehensive Ansible collection for setting up and managing terminal environments on macOS and Linux systems. This collection provides a clean, modular approach to installing terminal productivity tools, language managers, and shell configurations.

## Features

- **Hybrid Installation Approach**: Uses Homebrew for basic tools and official installers for language managers
- **Modular Design**: Separate roles for different concerns (tools, languages, shell config, scripts)
- **Profile-Based Setup**: Predefined profiles (minimal, developer, full) for different use cases
- **Smart Shell Configuration**: Manages PATH, environment variables, and tool initialization
- **Script Repository Management**: Clone and link personal/team script repositories
- **Cross-Platform Support**: Works on macOS (Darwin) and Linux systems
- **Idempotent Operations**: Safe to run multiple times without side effects

## Quick Start

1. **Install the collection:**
   ```bash
   ansible-galaxy collection install oreillyauto.terminal
   ```

2. **Run a simple setup:**
   ```bash
   ansible-playbook -i localhost, oreillyauto.terminal.local_setup
   ```

## Architecture

### Roles

- **`basic_tools`**: Installs terminal productivity tools via Homebrew
- **`language_managers`**: Installs language version managers via official installers
- **`shell_config`**: Manages shell configuration, PATH, and environment variables
- **`script_repos`**: Clones git repositories and symlinks scripts to `~/.local/bin`
- **`terminal_profile`**: Orchestrator role that combines other roles based on profiles

### Installation Methods

- **Homebrew Tools**: fzf, bat, eza, zoxide, direnv, uv, starship, sheldon, ripgrep, kubectl, jenkins-cli, gh, gcloud
- **Official Installers**: nvm, pyenv, rustup, sdkman (via curl scripts)
- **Archive Downloads**: Go (automated download and extraction)

## Profiles

### Minimal Profile
Basic terminal tools only, no shell configuration:
- fzf, bat, eza, ripgrep

### Developer Profile (Default)
Full development environment with language managers:
- All basic tools plus zoxide, direnv, uv, starship, sheldon, kubectl, jenkins-cli, gh, gcloud
- Language managers: nvm, pyenv, rustup, go, sdkman
- Shell configuration enabled

### Full Profile
Complete setup including script repository management:
- Everything from developer profile
- Script repository cloning and linking enabled

## Usage Examples

### Basic Usage

```yaml
- name: "Setup Terminal Environment"
  hosts: localhost
  connection: local
  tasks:
    - name: "Setup developer profile"
      ansible.builtin.include_role:
        name: oreillyauto.terminal.terminal_profile
      vars:
        terminal_profile: "developer"
```

### Custom Profile

```yaml
- name: "Custom Terminal Setup"
  hosts: localhost
  connection: local
  vars:
    terminal_profile: "developer"
    terminal_profile_custom_basic_tools:
      - "htop"
      - "tree"
    terminal_profile_custom_language_managers:
      - name: "rbenv"
        method: "curl"
        url: "https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer"
  tasks:
    - name: "Setup custom profile"
      ansible.builtin.include_role:
        name: oreillyauto.terminal.terminal_profile
```

### Individual Role Usage

```yaml
- name: "Install Basic Tools Only"
  hosts: localhost
  connection: local
  tasks:
    - name: "Install terminal tools"
      ansible.builtin.include_role:
        name: oreillyauto.terminal.basic_tools
      vars:
        basic_tools_list:
          - "fzf"
          - "bat"
          - "eza"
```

## Shell Configuration

The collection manages shell configuration through templated initialization blocks that are added to your `.zshrc` and `.bashrc` files. This includes:

### PATH Management
- Homebrew paths (`/opt/homebrew/bin`, `/usr/local/bin`)
- Local user paths (`~/.local/bin`, `~/.cargo/bin`)
- Language manager paths (pyenv, go, etc.)

### Environment Variables
- `GOROOT`, `PYENV_ROOT`
- `DOCKER_HOST`, `VAULT_ADDR`
- `FZF_DEFAULT_OPTS`, `EDITOR`, `PAGER`
- And more sane defaults

### Tool Initialization
- Starship prompt: `eval "$(starship init zsh)"`
- Zoxide: `eval "$(zoxide init zsh)"`
- Direnv: `eval "$(direnv hook zsh)"`
- Language managers (nvm, pyenv, rustup, sdkman)

### Default Configurations
- Git user configuration
- Starship prompt configuration (starship.toml)
- Sheldon plugin manager configuration (plugins.toml)

## Script Repository Management

Configure git repositories containing scripts to be cloned and linked:

```yaml
script_repositories:
  - name: "personal_scripts"
    repo: "git@github.com:user/scripts.git"
    path_in_repo: "bin"          # Subdirectory containing executables
    version: "main"              # Branch/tag/commit
    dest: "~/.local/src/personal_scripts"
```

Scripts are automatically symlinked to `~/.local/bin` and become available in your PATH.

## Requirements

- **Ansible**: 2.15 or higher
- **Collections**: `community.general`
- **macOS**: Homebrew must be installed
- **Linux**: Package manager support varies by distribution

## Installation

### From Ansible Galaxy

```bash
ansible-galaxy collection install oreillyauto.terminal
```

### From Source

```bash
git clone https://github.com/oreillyauto/ansible-terminal-collection.git
cd ansible-terminal-collection
ansible-galaxy collection build
ansible-galaxy collection install oreillyauto-terminal-*.tar.gz
```

## Customization

### Adding Custom Tools

Extend profiles with additional tools:

```yaml
terminal_profile_custom_basic_tools:
  - "htop"
  - "tree"
  - "jq"
```

### Custom Shell Configuration

Override default shell settings:

```yaml
shell_aliases:
  ll: "eza -la --git"
  cat: "bat"
  find: "fd"

shell_environment_vars:
  EDITOR: "nvim"
  PAGER: "less -R"
```

### Custom Language Managers

Add additional language managers:

```yaml
terminal_profile_custom_language_managers:
  - name: "rbenv"
    method: "curl"
    url: "https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer"
```

## Troubleshooting

### PATH Issues
If tools aren't found after installation:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Homebrew Not Found
Ensure Homebrew is installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Language Manager Issues
Language managers install to user directories and may require shell restart:
```bash
exec $SHELL -l
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: [Report bugs and feature requests](https://github.com/oreillyauto/ansible-terminal-collection/issues)
- Documentation: This README and role-specific documentation
- Examples: See `playbooks/` directory for usage examples
