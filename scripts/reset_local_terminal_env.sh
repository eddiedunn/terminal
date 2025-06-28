#!/usr/bin/env bash
set -euo pipefail

# This script removes all traces of the eddiedunn.terminal local setup playbook from your environment.
# It is intended for development and test purposes only!

# Remove core directories and completions
rm -rf ~/.local/bin
rm -rf ~/.config/shell_init.d
rm -rf ~/.bash_completion.d
rm -rf ~/.zsh/completions
rm -rf ~/.config/fish/completions

# Remove tool-specific directories
rm -rf ~/.nvm
# WARNING: Deleting ~/.pyenv will break all Python virtual environments created with Pyenv.
# Uncomment the next line ONLY if you want to fully remove all Pyenv-managed Pythons.
# rm -rf ~/.pyenv
rm -rf ~/.cargo
rm -rf ~/.sheldon
rm -rf ~/.fzf
rm -rf ~/.config/starship.toml
rm -rf ~/.config/starship
rm -rf ~/.config/bat
rm -rf ~/.config/eza
rm -rf ~/.config/zoxide
rm -rf ~/.config/direnv
rm -rf ~/.config/uv

# Remove shell init snippets for tools
rm -f ~/.config/shell_init.d/10-nvm.sh
rm -f ~/.config/shell_init.d/10-pyenv.sh
rm -f ~/.config/shell_init.d/10-rustup.sh

# FIX: Completely delete the shell configuration files for a true reset.
for shellrc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
  echo "[reset] Deleting $shellrc if it exists..."
  rm -f "$shellrc"
  # Also remove any stray backups from previous sed runs
  rm -f "${shellrc}.bak"
done

# Remove the artifact cache (hard-coded path)
rm -rf /tmp/terminal-ansible-artifacts

echo "[reset_local_terminal_env.sh] Reset complete. Please restart your shell."
