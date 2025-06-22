# Ansible Role: user_setup

This role is part of the `your_namespace.terminal` collection.

It is responsible for setting up the foundational user environment, including:
- Creating base directories like `~/.local/bin` and `~/.config`.
- Deploying generic dotfiles (`.gitconfig`, `.vimrc`, etc.).
- Managing shell configuration files (`.bashrc`, `.zshrc`) with managed blocks.
- Sourcing a standard directory (`~/.config/shell_init.d`) where other roles can place initialization scripts.
- Managing custom user-defined aliases and environment variables.

## Role Variables

- `user_setup_custom_aliases`: A dictionary of aliases to add.
- `user_setup_environment_variables`: A dictionary of environment variables to set.

**Usage:**
- To enable, add `nvm` and/or `pyenv` to your `terminal_setup_profile_tools`.
- After running the playbook, use `nvm install <version>` / `nvm use <version>` for Node.js, and `pyenv install <version>` / `pyenv global <version>` for Python.
- All setup is user-local; no root is required except for installing system dependencies.

This mechanism is extensible to other tools that are installed via git clone and shell integration.

---

## Rust/Cargo Development Environment

If you include `rustup` in your `terminal_setup_profile_tools` list, the role will:

1.  **Install all required system-level build dependencies** for the target OS (Debian/Ubuntu via `apt`, macOS via `brew`). This step uses `become: true`.
2.  **Download and execute the official `rustup-init.sh` script**, installing `rustup`, `cargo`, `rustc`, and the standard toolchain into the user's home directory (`~/.rustup` and `~/.cargo`).
3.  **Ensure `~/.cargo/bin` is added to the `PATH`** in your shell configuration files, making all Rust tools available in new shell sessions.

**Usage:**
- To enable, add `rustup` to your `terminal_setup_profile_tools`.
- After running the playbook, use `cargo build`, `rustc`, etc. You can manage toolchains with `rustup toolchain install nightly`.
- All setup is user-local; no root is required except for installing system dependencies.

---

## Ad-Hoc Script Management (via Git)

This role supports installing your own personal scripts from one or more Git repositories. This is the recommended way to manage your private scripts (like those in your `gdunn6_global_scripts` repo) without adding them directly to this Ansible role.

To use this feature, define the `terminal_setup_script_repos` variable in your playbook. It should be a list of dictionaries, where each dictionary has the following keys:

-   **`name`**: A unique name for the repository (used for the local cache directory, e.g., `my_scripts`).
-   **`repo`**: The SSH or HTTPS URL of the Git repository.
-   **`path_in_repo`** (optional): The subdirectory within the repo that contains your scripts. Defaults to `scripts`.
-   **`version`** (optional): The branch, tag, or commit to check out. Defaults to `main`.

The role will clone the repository to `~/.local/src/<name>` and then create symlinks in `~/.local/bin` for every executable file found in the specified `path_in_repo`. It will also automatically remove any symlinks from a previous run if the corresponding script was deleted from the repository, ensuring your `bin` directory stays in sync.

---

## Requirements

*   **Ansible Controller:** Ansible 2.10+ (for `ansible.builtin.blockinfile` and other modern features).
*   **Target Linux/macOS Host:**
    *   Bash or Zsh shell.
    *   Standard utilities like `tar`, `gzip`.
    *   User write access to `~/.local/bin` and `~/.config`.
    *   Architectures supported: `x86_64` and `aarch64` (Apple Silicon).
    *   For nvm/pyenv: ability to install dependencies via `apt` (Debian/Ubuntu) or `homebrew` (macOS).
*   **Pre-downloaded Binaries:** This role works with pre-downloaded binaries. A helper playbook is included to download all necessary binaries for supported platforms (Linux/macOS) and architectures (`x86_64`/`aarch64`) into the `roles/terminal_setup/files/` directory with the correct naming scheme (e.g., `starship-linux-x86_64`, `sheldon-darwin-aarch64`).

## Configuration

This role is configured by defining a list of desired tools in the `terminal_setup_profile_tools` variable. This declarative approach allows you to easily create different terminal "profiles" for different hosts or users.

All tool versions are managed within the role's `defaults/main.yml` file. Binaries are now detected automatically from the `files/` directory structure. You only need to provide the list of tool names.

### Advanced Configuration Options

While the main configuration is done through `terminal_setup_profile_tools`, you can also customize these advanced settings if needed:

*   `terminal_setup_managed_block_marker`: (string, default: `"# {mark} ANSIBLE MANAGED BLOCK (terminal_setup)"`)
    The marker used by `ansible.builtin.blockinfile` to delineate the managed configuration block in shell config files.
*   `terminal_setup_custom_aliases`: (dictionary, default: `{}`)
    A dictionary of ad-hoc aliases to add to the user's shell. This allows you to define custom aliases directly in your playbook without modifying the role's defaults. See the example below.
*   `terminal_setup_script_repos`: (list of dictionaries, default: `[]`)
    A list of Git repositories containing personal scripts to be installed into the user's `~/.local/bin`. See the "Ad-Hoc Script Management" section for details.

## Role Tasks

**All tasks are conditional:** The following steps only occur if `terminal_setup_enabled` is `true` and at least one feature flag is enabled. Feature-specific steps only occur if their flag is enabled.

The role performs the following actions on the target Linux/macOS host (if enabled):

1.  Ensures the user's local binary directory (`~/.local/bin`) and configuration directories exist.
2.  Determines the target's OS and architecture (`ansible_os_family`, `ansible_architecture`).
3.  Copies the correct pre-downloaded binary (e.g., `files/starship-linux-x86_64` or `files/starship-darwin-aarch64`) to `~/.local/bin/starship` and makes it executable.
4.  Deploys template files like `plugins.toml.j2` and `starship.toml.j2` to the user's config directory.
5.  Manages a block of shell configuration in `~/.bashrc` to initialize the environment.
6.  Manages similar blocks in `~/.zshrc` and `~/.zshenv` for Zsh environments.
7.  Installs nvm and/or pyenv if enabled, including all required dependencies and shell initializations.

## Preparing Binaries

This role expects you to provide the executables for all required tools, operating systems, and architectures. A helper playbook is provided to automate this process.

1.  **Run the Helper Playbook:**
    From your Ansible project's root directory, run the helper playbook. This playbook reads the tool definitions from `defaults/main.yml`, downloads all binary variants, and places the executables in the correct location (`roles/terminal_setup/files/`) with the correct names.

    ```bash
    ansible-playbook playbooks/terminal_setup_download_binaries.yml
    ```

    The playbook will automatically download, verify, and extract the correct binaries for your configured versions into the role's `files/` directory, ready for deployment.

## nvm and pyenv

If enabled, nvm and/or pyenv are installed in userland with all required dependencies. Their shell initialization is injected into the managed shell snippet for Bash and Zsh. This allows you to use `nvm` and `pyenv` commands immediately in every new shell session.

- **nvm**: Manage multiple Node.js versions per user. After install, use `nvm install <version>` and `nvm use <version>`.
- **pyenv**: Manage multiple Python versions per user. After install, use `pyenv install <version>` and `pyenv global <version>`.

Dependencies are installed via apt (Debian/Ubuntu) or homebrew (macOS) as needed. See `tasks/main.yml` for the full list.

## Template Structure

The role uses a consistent snippet-based template system for all configuration files. Each template follows the pattern `*_snippet.j2` and is designed to be extensible through the `terminal_setup_tools_processed` data structure.

### Core Configuration Files

*   **Sheldon (`templates/plugins_snippet.j2`):** 
    Manages shell plugins through Sheldon. The template dynamically generates plugin configurations based on the `terminal_setup_tools_processed` list. Each tool can define its Sheldon plugin configuration using the `sheldon_plugin` property.
    
    Example tool definition in `defaults/main.yml`:
    ```yaml
    - name: zoxide
      sheldon_plugin: |
        github = "ajeetdsouza/zoxide"
        apply = ["source"]
    ```

*   **Starship (`templates/starship.toml.j2`):** 
    Configures the Starship prompt. Customize this template to modify prompt appearance and behavior. See the [Starship documentation](https://starship.rs/config/) for all available options.

### Shell Configuration Snippets

*   **Bash (`templates/bashrc_snippet.j2`):** 
    Bash-specific configuration loaded by `~/.bashrc`. Initializes tools, sets up environment variables, and sources tool-specific configurations.

*   **Zsh (`templates/zshrc_snippet.j2`):**
    Zsh-specific configuration loaded by `~/.zshrc`. Includes Zsh-specific initializations and tool configurations.

*   **Environment (`templates/zshenv_snippet.j2`):**
    Environment variable configuration loaded by `~/.zshenv`. Sets up PATH and other environment variables for both interactive and non-interactive shells.

### Tool-Specific Configuration

*   **Git (`templates/gitconfig_snippet.j2`):**
    Global Git configuration. Can be extended by tools through the `gitconfig` property in `terminal_setup_tools_processed`.

*   **Vim (`templates/vimrc_snippet.j2`):**
    Vim configuration file. Tools can add Vim-specific settings through the `vimrc` property.

*   **Bash Aliases (`templates/bash_aliases_snippet.j2`):**
    Global bash aliases. Tools can define aliases using the `aliases` property in their configuration.

*   **Global Gitignore (`templates/gitignore_global_snippet.j2`):**
    Global Git ignore rules. Tools can add patterns through the `gitignore` property.

### Extending Configuration

Each tool in `terminal_setup_tools_processed` can contribute to multiple configuration files by defining the appropriate properties:

```yaml
- name: my_tool
  state: present
  aliases:  # For bash_aliases_snippet.j2
    mt: "my_tool --flag"
  env_vars:  # For zshenv_snippet.j2
    MY_TOOL_PATH: "{{ ansible_user_dir }}/.local/my_tool"
  vimrc: |  # For vimrc_snippet.j2
    " My Tool Vim Settings
    let g:mytool_enabled = 1
  gitconfig: |  # For gitconfig_snippet.j2
    [mytool]
    path = ~/projects/mytool
  gitignore: |  # For gitignore_global_snippet.j2
    # My Tool temporary files
    *.mytool.cache
    .mytool_temp/
```

This modular approach allows for easy extension and customization of the terminal environment while maintaining a clean separation of concerns.

### Example: Starship Configuration

Customize your prompt by editing `templates/starship.toml.j2`. Here's an example configuration:

```toml
# ~/.config/starship.toml

# Add a newline before the prompt
add_newline = true

[username]
show_always = true
style_user = "bold fg:green"
style_root = "bold fg:red"

[hostname]
ssh_only = false
style = "bold fg:blue"
disabled = false

# Show current directory
[directory]
truncation_length = 8
truncate_to_repo = true
style = "blue"

# Git integration
[git_branch]
format = "on [$symbol$branch]($style) "
style = "green"

[git_status]
style = "yellow"
```

For more customization options, refer to the [Starship documentation](https://starship.rs/config/).

## Example Playbook

To set up a full developer environment with Starship, Sheldon, fzf, bat, nvm, pyenv, and a Rust toolchain:

```yaml
---
- name: Setup Developer Terminal Environment
  hosts: workstations
  become: false
  roles:
    - role: terminal_setup
      vars:
        terminal_setup_profile_tools:
          - starship
          - sheldon
          - fzf
          - bat
          - nvm
          - pyenv
          - rustup
```

To configure a minimal setup for a server **with custom aliases and scripts from a Git repo**:

```yaml
---
- name: Setup Server Terminal Environment
  hosts: webservers
  become: false
  roles:
    - role: terminal_setup
      vars:
        terminal_setup_profile_tools:
          - fzf
          - bat
        terminal_setup_custom_aliases:
          k: "kubectl"
          kgp: "kubectl get pods -A"
          ".." : "cd .."
        terminal_setup_script_repos:
          - name: "gdunn6_global_scripts"
            repo: "https://github.com/user/my-scripts.git"
            path_in_repo: "scripts"
            version: "main"
```

To disable the role entirely (no-op):

```yaml
- name: Disable terminal setup
  hosts: all
  roles:
    - role: terminal_setup
      vars:
        terminal_setup_enabled: false
```

After running the playbook, users will need to log out and log back in, or source their `~/.bashrc` or `~/.zshrc` for the changes to take effect.

## Helper Playbook for Downloading Binaries (Controller-Side)

A sample playbook `playbooks/download_role_binaries.yml.example` might look like this:

```yaml
# playbooks/download_role_binaries.yml.example
# Run this playbook on your Ansible controller to download binaries.
---
- name: Download binaries for terminal_setup role
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Include download tasks from terminal_setup role
      ansible.builtin.include_role:
        name: terminal_setup
        tasks_from: download_binaries.yml
```

Run it with: `ansible-playbook playbooks/download_role_binaries.yml.example`
You can update all required binaries automatically using:

```bash
ansible-playbook playbooks/download_terminal_setup_binaries.yml -i 'localhost,'
```

This will download, verify, and extract the correct binaries for your configured versions. Follow any on-screen instructions to update checksum variables as needed.

Remember to then manually extract the executables from `/tmp/` and place them into `roles/terminal_setup/files/` if not automated.
