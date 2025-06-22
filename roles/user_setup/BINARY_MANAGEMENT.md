# Terminal Setup Role: Binary & Extras Management Design

## Overview
This document describes the actual, current system for managing CLI tool binaries and completions in the modular Ansible collection. The system is fully automated, rootless, and cross-platform, and is now split into two main data sources:

- **Binaries:** Defined in `defaults/main.yml` for each tool, per OS/arch, with download/extract rules.
- **Completions:** Defined centrally in `files/completions_metadata.yml` for each tool and shell, with download/generation rules.

The `download_helper.py` script orchestrates both binaries and completions, staging all necessary files in the role's `files/` directory for later installation by the role.

---

## Data Model: Binaries and Completions

### Binaries (in `defaults/main.yml`)
Each tool is defined with a flexible schema, for example:

```yaml
- name: sheldon
  version: "0.8.2"
  description: "A fast, configurable, shell plugin manager."
  install_type: binary
  binaries:
    Darwin:
      aarch64:
        url: "https://github.com/rossmacarthur/sheldon/releases/download/0.8.2/sheldon-0.8.2-aarch64-apple-darwin.tar.gz"
        executable_in_archive: "sheldon"
        checksum: "..."
```

### Completions (in `files/completions_metadata.yml`)
Completions are NOT embedded in the tool YAML. Instead, they are defined in a dedicated metadata file, for example:

```yaml
completions:
  - name: zoxide
    zsh:
      method: cli
      command: "zoxide init zsh --cmd z"
      output: "zoxide.zsh"
    bash:
      method: cli
      command: "zoxide init bash --cmd z"
      output: "zoxide.bash"
```

---

## Download & Staging Process
- The `download_helper.py` script reads `defaults/main.yml` and `completions_metadata.yml`.
- Binaries are downloaded and extracted as specified.
- Completions are downloaded or generated (via CLI or URL) as specified.
- All files are staged in `roles/<role>/files/` for later copying by the Ansible role.

---

## Installation Process
- The Ansible role copies binaries from staged files to the user's `~/.local/bin/`.
- Completions are copied from staged files to the user's completions directory (e.g., `~/.zsh/completions`).

---

## Notes
- All logic is now data-driven and split between binaries (main.yml) and completions (completions_metadata.yml).
- No completions/extras are embedded in the main tool YAML.
- Documentation and implementation are now aligned.

## Supported Keys
### Binaries
| Key                   | Description                                                |
|-----------------------|-----------------------------------------------------------|
| `url`                 | Download URL for the binary archive or raw binary         |
| `executable_in_archive` | Path to the binary inside the archive (if not root)      |
| `checksum`            | (Optional) SHA256 or other checksum for integrity check   |

### Completions/Extras (per shell or purpose)
| Key                   | Description                                                |
|-----------------------|-----------------------------------------------------------|
| `source`              | Path inside the main archive to the file                  |
| `url`                 | (Optional) Separate archive or file URL                   |
| `archive_type`        | (Optional) Archive type (`tar.gz`, `zip`, etc.)           |
| `executable_in_archive` | (Optional) Path in the archive to the file               |
| `dest`                | Destination path relative to user home                    |

---

## Downloader Script Responsibilities
- For each tool, OS, and arch:
  - Download the binary archive or file from `url`.
  - Extract `executable_in_archive` if specified, else autodetect.
  - Verify `checksum` if provided.
  - Place binary at:  
    `roles/terminal_setup/files/{os}/{arch}/{tool}/{version}/{tool}`
- For each completion or extra (per tool, per shell/purpose):
  - If `url` is present, download and extract the specified file.
  - If only `source`, extract from the main archive.
  - Place at:  
    `roles/terminal_setup/files/completions/{tool}/{version}/{shell}/` or
    `roles/terminal_setup/files/extras/{tool}/{version}/{purpose}/`
- **Data-driven:** All logic is based on the YAML schema; no hardcoded tool rules.

---

## Ansible Role Responsibilities
- Copy binaries from role files to the user’s `~/.local/bin/` or similar.
- For each completion/extra, copy from role files to the user’s specified `dest`.
- Update shell configuration to source completions if present.
- Skip any items not defined for the current OS/arch/shell.

---

## Shell Configuration Snippets
**Bash:**
```bash
for f in ~/.local/share/bash-completion/completions/*; do
  [ -f "$f" ] && . "$f"
done
```
**Zsh:**
```zsh
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

---

## Adding a New Tool or File Type
1. Add a YAML entry for the tool with `binaries`, `completions`, and/or `extras` as needed.
2. Specify all URLs, archive paths, and destinations explicitly.
3. The downloader and role will process everything automatically.

---

## Design Goals
- **Per-app, per-file-type flexibility**
- **No hardcoding:** Everything is data-driven from YAML
- **Extensible:** New tools, shells, or file types require only YAML edits
- **Robust:** Handles main and separate archives, any directory structure, and multiple file types

---

## FAQ / Gotchas

**Q: Do I need to install the `fzf` binary if I load the fzf Zsh plugin via Sheldon?**

**A:** No. If you have the `fzf-zsh-plugin` loaded through Sheldon (as defined in `terminal_setup_sheldon_plugins`), you do not need to install the `fzf` binary separately for Zsh completions and keybindings. The plugin provides all Zsh integration. Only install the `fzf` binary if you want the standalone `fzf` CLI tool or use it outside Zsh.

_This document is the contract for binary, completions, and extras management in the terminal_setup role. All implementation should follow this schema and process._
