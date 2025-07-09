#!/usr/bin/env bash
set -euo pipefail

# Reset the terminal environment for the dedicated appuser account. This mirrors
# reset_local_terminal_env.sh but operates on the appuser home directory.

TARGET_USER="appuser"
HOME_DIR="$(eval echo ~${TARGET_USER})"

# Remove core directories and completions
rm -rf "$HOME_DIR/.local/bin"
rm -rf "$HOME_DIR/.config/shell_init.d"
rm -rf "$HOME_DIR/.bash_completion.d"
rm -rf "$HOME_DIR/.zsh/completions"
rm -rf "$HOME_DIR/.config/fish/completions"

# Remove tool-specific directories
rm -rf "$HOME_DIR/.nvm"
# WARNING: Deleting ~/.pyenv will break all Python virtual environments created with Pyenv.
# Uncomment the next line ONLY if you want to fully remove all Pyenv-managed Pythons for appuser.
# rm -rf "$HOME_DIR/.pyenv"
rm -rf "$HOME_DIR/.cargo"
rm -rf "$HOME_DIR/.sheldon"
rm -rf "$HOME_DIR/.fzf"
rm -rf "$HOME_DIR/.config/starship.toml"
rm -rf "$HOME_DIR/.config/starship"
rm -rf "$HOME_DIR/.config/bat"
rm -rf "$HOME_DIR/.config/eza"
rm -rf "$HOME_DIR/.config/zoxide"
rm -rf "$HOME_DIR/.config/direnv"
rm -rf "$HOME_DIR/.config/uv"

# Remove shell init snippets for tools
rm -f "$HOME_DIR/.config/shell_init.d/10-nvm.sh"
rm -f "$HOME_DIR/.config/shell_init.d/10-pyenv.sh"
rm -f "$HOME_DIR/.config/shell_init.d/10-rustup.sh"

# Remove lines sourcing shell_init.d from shell configs
sed -i.bak '/shell_init\.d/d' "$HOME_DIR/.bashrc" 2>/dev/null || true
sed -i.bak '/shell_init\.d/d' "$HOME_DIR/.zshrc" 2>/dev/null || true
sed -i.bak '/shell_init\.d/d' "$HOME_DIR/.profile" 2>/dev/null || true

# Remove the artifact cache (hard-coded path)
rm -rf /tmp/terminal-ansible-artifacts

# Optionally remove backup files created by sed
rm -f "$HOME_DIR/.bashrc.bak" "$HOME_DIR/.zshrc.bak" "$HOME_DIR/.profile.bak"

echo "[reset_appuser_terminal_env.sh] Reset complete for ${TARGET_USER}. Please restart the shell."
