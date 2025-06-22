# FZF Integration Policy for terminal_setup Role

## Overview
This document describes how the `terminal_setup` Ansible role manages FZF (fuzzy finder) integration across different environments and plugin manager configurations. It is intended to clarify how FZF is installed and configured, and how the role interacts with plugin managers like Sheldon and prompt engines like Starship.

---

## FZF Integration Scenarios

### 1. Standalone FZF (No Sheldon, No Starship)
- **Supported:** YES
- **Behavior:**
  - The role installs the FZF binary.
  - Deploys completions and keybindings for all supported shells (Zsh, Bash, Fish).
  - Injects the required shell initialization code directly.
- **Intended for:** Minimal/production environments where only FZF is desired and plugin managers are not available or not allowed.

### 2. With Sheldon (Plugin Manager)
- **Supported:** YES
- **Behavior:**
  - If Sheldon is enabled and the `fzf-zsh-plugin` is present in `~/.config/sheldon/plugins.toml`, Sheldon manages FZF's Zsh integration (keybindings, completions, functions).
  - The role **skips manual FZF Zsh completions/keybindings** to avoid conflicts or double-sourcing.
  - For Bash and Fish, the role continues to manage FZF completions.
- **Note:** If Sheldon is present but NOT managing FZF, the role will proceed with manual setup for Zsh as well.

### 3. With Starship (Prompt Engine)
- **Supported:** YES
- **Behavior:**
  - Starship does NOT manage FZF or its integration. The presence or absence of Starship does not affect FZF setup.

### 4. With Both Sheldon and Starship
- **Behavior:**
  - Same as scenario 2: Sheldon manages Zsh FZF integration, Starship is ignored for FZF setup.

---

## Implementation Policy
- **Default:**
  - The role always installs and configures FZF for all enabled shells unless Sheldon is present and managing the Zsh plugin.
- **Conditional Logic:**
  - If `fzf` is enabled AND Sheldon is present AND the `fzf-zsh-plugin` is listed in plugins.toml, the role skips manual Zsh FZF setup.
  - Otherwise, the role ensures FZF is fully set up for all shells.
- **No dependency on Starship for FZF integration.**

---

## Why This Policy?
- To ensure FZF is always available and fully integrated, even in minimal/production environments.
- To prevent double-configuration/conflicts when using plugin managers.
- To provide a clear, predictable experience for all users and environments.

---

## Example: Minimal FZF-Only Setup
```yaml
terminal_setup_profile_tools:
  - fzf
```
- This will install FZF and set up completions/integration for all shells, even if Sheldon/Starship are not present.

---

## Questions?
If you have questions or need to extend this logic for other tools, see the role README or contact the maintainers.
