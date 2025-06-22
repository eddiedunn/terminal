# Completions Workflow for `terminal_setup` Role

This document explains how shell completions are managed in this role for Zsh, Bash, and Fish in a reproducible, userland-friendly way.

---

## Overview

- **Completions for supported tools are staged during the download step** (using the download helper script and completions_metadata.yml).
- **The Ansible role then copies these pre-populated completions** into the user's completions directory at install time.
- **No completions are generated or extracted at runtime**—everything is staged and idempotent.

---

## How It Works

### 1. Download Step
- Run the download playbook (e.g., `ansible-playbook playbooks/terminal_setup_download_binaries.yml`).
- This will:
  - Download all required binaries.
  - Parse `files/completions_metadata.yml` for completions for each tool and shell.
  - For each completion:
    - If `method: cli`, runs the CLI to generate the completion script.
    - If `method: url`, downloads the completion script from the upstream URL.
    - If `method: archive`, (future) will extract from the tool's archive.
    - If `method: plugin` or `none`, does nothing (handled by plugin manager or not needed).
  - Stages all completions in `roles/terminal_setup/files/completions/<shell>/`.

### 2. Role Install Step
- When the main role is run, it copies the staged completions from `files/completions/<shell>/` to the user's completions directory:
  - Zsh: `~/.zsh/completions`
  - Bash: `~/.bash_completion.d`
  - Fish: `~/.config/fish/completions`
- The user's shell config should source these directories (see role templates for examples).

---

## Adding or Updating Completions
- Edit `files/completions_metadata.yml` to add or update completions for any tool or shell.
- Rerun the download playbook to re-stage completions.
- The main role will pick up any new completions automatically at install time.

---

## Why This Approach?
- **Reproducible:** All completions are staged and versioned with the role.
- **Userland:** No root or system-wide changes; all completions are installed in the user’s home directory.
- **Extensible:** Easy to add new tools or shells by editing a single metadata file.
- **Fast:** No runtime extraction or generation—just a file copy.

---

For more details, see `files/completions_metadata.yml` and the download helper script.
