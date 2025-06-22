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

## Quickstart
1. Clone the repo
2. Create and activate the virtual environment (if not already present):
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run molecule/ansible/pytest commands as needed (with the venv activated)

---

## Reference: Source Role
- Role name: `terminal_setup`
- Path: `/Users/tmwsiy/code/gaia-infra-platform/ansible/roles/terminal_setup`

---

**Always activate the environment!**
