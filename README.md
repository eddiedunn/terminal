# Terminal Ansible Collection

A modular Ansible collection to configure a modern, cross-platform terminal environment with your favorite userland tools, dotfiles, and developer shell workflows.

## Features

- **Declarative Tool Management**: Define your desired tools and versions in a single YAML file.
- **Controller-Side Artifact Cache**: Binaries are downloaded and verified once on the controller, enabling fast, reproducible, and offline-capable deployments to multiple hosts.
- **Cross-Platform**: Natively supports Linux (Debian/Ubuntu) and macOS (aarch64/x86_64).
- **Robust Shell Integration**: Idempotently manages shell initialization scripts, completions, and environment variables without mangling user `.*rc` files.
- **Extensible**: Easily add new tools, completions, or even entire installation roles (like `nvm` or `pyenv`).
- **Orchestrated Profiles**: The `profile` role acts as a simple, high-level interface to compose your perfect terminal environment.

---

## Quick Start (Local Setup)

This playbook will configure the terminal for the current user on your local machine.

1.  **Prerequisites**: Ensure you have Python, `pip`, and `venv` installed.
2.  **Clone the Repository**:
    ```sh
    git clone https://github.com/eddiedunn/terminal.git
    cd terminal
    ```
3.  **Set up the Environment**:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
4.  **Run the Local Setup Playbook**:
    ```sh
    ansible-playbook playbooks/local_setup.yml
    ```
    This command will automatically:
    - Build and install the collection locally.
    - Run the `download_helper.py` script to stage all necessary binaries.
    - Execute the Ansible playbook to configure your system.

---

## Architecture Overview

This collection is designed with a clear separation of concerns:

1.  **Artifact Staging (Controller)**: The `download_helper.py` script is executed first on the Ansible controller. It reads tool definitions from `roles/tool_installer/defaults/main.yml` and `roles/tool_installer/files/completions_metadata.yml`, downloads all required binaries and completion scripts, verifies their checksums, and places them into an artifact cache (default: `/tmp/terminal-ansible-artifacts`). This makes subsequent runs fast and enables offline provisioning.

2.  **Orchestration (`profile` role)**: This is the main entry point. It orchestrates other roles based on the tools you've defined in the `profile_tools` variable.

3.  **Core Engines (`tool_installer`, `nvm`, etc.)**:
    - `tool_installer`: Copies pre-staged binaries and completions from the controller's cache to the target machine. It also deploys shell initialization snippets.
    - `system_dependencies`: Installs system-level packages (e.g., `build-essential`) required by other roles.
    - `nvm`, `pyenv`, `rustup`: Handle tools that require script-based git checkouts and have their own initialization logic.

---

## Customization

To customize your setup, edit `playbooks/local_setup.yml` (or your own playbook) and modify the `vars` section:

```yaml
# playbooks/local_setup.yml
- name: Setup Local Terminal Environment
  hosts: localhost
  connection: local
  vars:
    # 1. Define which tools you want to install
    profile_tools:
      - starship
      - sheldon
      - fzf
      - bat
      - eza
      - ripgrep
      - zoxide
      - direnv
      - nvm  # Example of a script-based installer

    # 2. Define which shells to configure
    profile_shells:
      - bash
      - zsh

    # 3. Add custom aliases and environment variables
    profile_custom_aliases:
      k: "kubectl"
      l: "eza -l"
    profile_environment_variables:
      EDITOR: "nvim"
      # ...
```

---

## For Developers & Contributors

- **Testing**: Each role includes a `molecule` scenario for independent testing.
  ```sh
  # Activate venv first!
  source .venv/bin/activate
  # Test a specific role
  cd roles/tool_installer
  molecule test
  ```
- **Binary Management**: For details on how binaries, checksums, and completions are managed, see `roles/tool_installer/README.md`.
- **Linting**: Run all linters with the helper script:
  ```sh
  ./scripts/lint_all.sh
  ```

---

### A Note on `eza` for macOS

The official `eza` project does not currently distribute pre-built binaries for Darwin (macOS). To provide a seamless out-of-the-box experience, this collection uses a public fork ([eddiedunn/eza](https://github.com/eddiedunn/eza)) that builds and releases these binaries. The source and build process are fully transparent. Should the official project begin publishing Darwin binaries, this collection will be updated to use them.


## Quickstart

1. **Clone the repo**
2. **Create and activate the Python virtual environment**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Run the local setup playbook**
   ```sh
   ansible-playbook playbooks/local_setup.yml
   ```

## Architecture Overview

- **tool_installer**: The engine. Installs tools, manages binaries, and drops shell init scripts.
- ****: The chassis. Prepares user directories, dotfiles, and configures the shell to source init scripts.
- **profile**: The blueprint. Orchestrates the other roles and defines the user-facing entry point.

## Documentation
- See `docs/BINARY_MANAGEMENT.md` for binary caching and reproducibility.
- See `docs/COMPLETIONS_WORKFLOW.md` for shell completions and FZF integration.

## Customization
- Edit `playbooks/local_setup.yml` to add/remove tools or configure shells, aliases, and environment variables.
- Override variables in your inventory or on the command line as needed.

## Testing
- Each role includes a `molecule` scenario for independent testing:
  ```sh
  cd roles/tool_installer && molecule test
  cd roles/ && molecule test
  ```

---

For advanced usage and details, see the `docs/` directory and each role's README.md.


**IMPORTANT: Activate the Python Virtual Environment Before Running Any Commands!**

Before running any Python, Ansible, or Molecule commands in this project, you MUST activate the virtual environment:

```sh
source .venv/bin/activate
```

This is required for all development, testing, and CI. If you skip this step, commands like `ansible-lint`, `molecule`, and `ansible-playbook` will fail or use the wrong dependencies.

---

## Project Structure
- Modular Ansible roles: ``, `tool_installer`, `nvm`, `pyenv`, `rustup`, `profile`
- Collection metadata: `galaxy.yml`, `.gitignore`

---

## Binary Management Philosophy & eza Darwin Binaries

This project includes pre-built binaries for several tools to ensure reproducible, offline, and cross-platform automation. One notable case is the inclusion of a Darwin (macOS) binary for [`eza`](https://github.com/eza-community/eza), a modern replacement for `ls`.

### Why a Custom Fork for eza?
The official `eza-community/eza` project does **not** distribute pre-built Darwin/macOS binaries. To provide a seamless experience for macOS users, this project uses a custom fork ([eddiedunn/eza](https://github.com/eddiedunn/eza)) to build and distribute the required Darwin binaries.

- **Transparency:** The source and build process for these binaries are publicly available. Users are encouraged to review the [eddiedunn/eza](https://github.com/eddiedunn/eza) fork and compare it with the official [eza-community/eza](https://github.com/eza-community/eza).
- **Rebuilding:** If you prefer to build your own binaries, you can do so by following the instructions in the fork or the official repo, then replacing the binary in the appropriate files directory.
- **Security & Trust:** This approach is documented here to ensure transparency. If/when the official project begins distributing Darwin binaries, this project will switch to using those official releases.

For details on how binaries and completions are managed, see `BINARY_MANAGEMENT.md`, `COMPLETIONS_WORKFLOW.md`, and the helper automation scripts included in the repository.

## Quickstart
1. Clone the repo
2. Create and activate the virtual environment (if not already present):
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

---

## Using This Collection in Your Ansible Project

To include this collection in your own Ansible repository:

1. **Add to `collections/requirements.yml`:**

   ```yaml
   ---
   collections:
     - name: <your_namespace>.terminal
       source: <path or URL to this collection>
   ```

   - If using locally, set `source` to the relative or absolute path.
   - **To install directly from this repository (development or private use):**
     1. Clone the repository:
        ```sh
        git clone https://github.com/eddiedunn/terminal.git
        ```
     2. Build and install the collection:
        ```sh
        ansible-galaxy collection build terminal
        ansible-galaxy collection install eddiedunn-terminal-*.tar.gz
        ```
   - **To install directly from git (if using Ansible 2.10+):**
     ```sh
     ansible-galaxy collection install git+https://github.com/eddiedunn/terminal.git
     ```
     > **Note:** This method cannot be used in `collections/requirements.yml` unless the repo is structured and tagged for Galaxy.
   - **If publishing to Ansible Galaxy:**
     Publish the collection, then users can add to `collections/requirements.yml`:
     ```yaml
     collections:
       - name: eddiedunn.terminal
     ```
     and install with:
     ```sh
     ansible-galaxy collection install -r collections/requirements.yml
     ```
## ⚡ Local Collection Development Best Practices

**1. Always run playbooks from the project root**
- Do not run playbooks from inside the collection directory. This ensures Ansible resolves roles and collections using the correct local paths.
2. **Install the collection:**

   ```sh
   ansible-galaxy collection install -r collections/requirements.yml
   ```

3. **Reference roles from the collection in your playbooks:**

   ```yaml
   - hosts: all
     roles:
       - role: <your_namespace>.terminal.
   ```

Replace `<your_namespace>` with the actual namespace (e.g., `eddiedunn`).

3. Stage all required binaries and completions by running:
   ```sh
   python3 roles//scripts/download_helper.py roles/
   ```
   This will read `defaults/main.yml` and `files/completions_metadata.yml`, download all binaries, and stage completions for all supported shells.
   - As of the current implementation, for zoxide, any 'eval' lines are stripped from the generated zoxide.zsh completion file to avoid double initialization.
   ```
3. Run molecule/ansible/pytest commands as needed (with the venv activated)

---

## Reference: Source Role
- Role name: `terminal_setup`
- Path: `/Users/tmwsiy/code/gaia-infra-platform/ansible/roles/terminal_setup`

---

**Always activate the environment!**
