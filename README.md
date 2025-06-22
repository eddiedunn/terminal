# Terminal Automation Ansible Collection

**IMPORTANT: Activate the Python Virtual Environment Before Running Any Commands!**

Before running any Python, Ansible, or Molecule commands in this project, you MUST activate the virtual environment:

```sh
source .venv/bin/activate
```

This is required for all development, testing, and CI. If you skip this step, commands like `ansible-lint`, `molecule`, and `ansible-playbook` will fail or use the wrong dependencies.

---

## Project Structure
- Modular Ansible roles: `user_setup`, `tool_installer`, `nvm`, `pyenv`, `rustup`, `profile`
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
   - To install directly from this repository, use the following URL for the `source` field:
     
     ```yaml
     collections:
       - name: eddiedunn.terminal
         source: https://github.com/eddiedunn/terminal.git
     ```
   - If publishing to Ansible Galaxy, use the Galaxy namespace and collection name.

2. **Install the collection:**

   ```sh
   ansible-galaxy collection install -r collections/requirements.yml
   ```

3. **Reference roles from the collection in your playbooks:**

   ```yaml
   - hosts: all
     roles:
       - role: <your_namespace>.terminal.user_setup
   ```

Replace `<your_namespace>` with the actual namespace (e.g., `eddiedunn`).

3. Stage all required binaries and completions by running:
   ```sh
   python3 roles/user_setup/scripts/download_helper.py roles/user_setup
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
