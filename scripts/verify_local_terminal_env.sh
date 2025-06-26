#!/usr/bin/env bash
set -euo pipefail

# This script verifies that the eddiedunn.terminal local setup playbook has completed its intended operations.
# It checks for key directories, files, binaries, and shell config changes.

failures=0

check_exists() {
  if [ ! -e "$1" ]; then
    echo "[FAIL] Missing: $1"
    failures=$((failures+1))
  else
    echo "[OK] Present: $1"
  fi
}

check_dir() {
  if [ ! -d "$1" ]; then
    echo "[FAIL] Missing directory: $1"
    failures=$((failures+1))
  else
    echo "[OK] Directory present: $1"
  fi
}

check_bin() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "[OK] On PATH: $1"
  elif [ -x "$HOME/.local/bin/$1" ]; then
    echo "[OK] $1 found in ~/.local/bin (not on PATH)"
  else
    echo "[FAIL] Not found: $1 (not on PATH or in ~/.local/bin)"
    failures=$((failures+1))
  fi
}

# Check core directories
check_dir "$HOME/.local/bin"
check_dir "$HOME/.config/shell_init.d"
check_dir "$HOME/.bash_completion.d"
check_dir "$HOME/.zsh/completions"
check_dir "$HOME/.config/fish/completions"

# Check tool-specific directories for version managers
for d in "$HOME/.nvm" "$HOME/.pyenv" "$HOME/.cargo"; do
  check_dir "$d"
done

# Check important shell init snippets
for f in "$HOME/.config/shell_init.d/10-nvm.sh" \
         "$HOME/.config/shell_init.d/10-pyenv.sh" \
         "$HOME/.config/shell_init.d/10-rustup.sh"; do
  check_exists "$f"
done

# Check for all installed binaries
for bin in starship sheldon fzf bat eza ripgrep zoxide direnv uv; do
  check_bin "$bin"
done

# Check artifact cache
if [ -d "/tmp/terminal-ansible-artifacts" ]; then
  echo "[OK] Artifact cache present: /tmp/terminal-ansible-artifacts"
else
  echo "[FAIL] Artifact cache missing: /tmp/terminal-ansible-artifacts"
  failures=$((failures+1))
fi

# Check for shell sourcing
for shellrc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
  if grep -q 'shell_init.d' "$shellrc" 2>/dev/null; then
    echo "[OK] $shellrc sources shell_init.d"
  else
    echo "[FAIL] $shellrc does not source shell_init.d"
    failures=$((failures+1))
  fi
done

if [ "$failures" -eq 0 ]; then
  echo "[verify_local_terminal_env.sh] All checks passed."
  exit 0
else
  echo "[verify_local_terminal_env.sh] $failures check(s) failed."
  exit 1
fi
