#!/usr/bin/env bash
set -euo pipefail

# Verify the terminal setup for the dedicated appuser account. This mirrors
# verify_local_terminal_env.sh but targets the appuser home directory.

TARGET_USER="appuser"
HOME_DIR="$(eval echo ~${TARGET_USER})"
USER_CMD=(sudo -Hiu "${TARGET_USER}" --)

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
  if "${USER_CMD[@]}" command -v "$1" >/dev/null 2>&1; then
    echo "[OK] On PATH: $1"
  elif [ -x "$HOME_DIR/.local/bin/$1" ]; then
    echo "[OK] $1 found in ~/.local/bin (not on PATH)"
  else
    echo "[FAIL] Not found: $1 (not on PATH or in ~/.local/bin)"
    failures=$((failures+1))
  fi
}

# Check core directories
check_dir "$HOME_DIR/.local/bin"
check_dir "$HOME_DIR/.config/shell_init.d"
check_dir "$HOME_DIR/.bash_completion.d"
check_dir "$HOME_DIR/.zsh/completions"
check_dir "$HOME_DIR/.config/fish/completions"

# Check tool-specific directories for version managers and language runtimes
for d in \
  "$HOME_DIR/.nvm" \
  "$HOME_DIR/.pyenv" \
  "$HOME_DIR/.cargo" \
  "$HOME_DIR/.sdkman" \
  "$HOME_DIR/.local/go" \
  "$HOME_DIR/go" \
  "$HOME_DIR/go/bin"; do
  check_dir "$d"
done

# Check important shell init snippets
for f in \
  "$HOME_DIR/.config/shell_init.d/00_path.sh" \
  "$HOME_DIR/.config/shell_init.d/10_environment.sh" \
  "$HOME_DIR/.config/shell_init.d/10-nvm.sh" \
  "$HOME_DIR/.config/shell_init.d/10-pyenv.sh" \
  "$HOME_DIR/.config/shell_init.d/10-rustup.sh" \
  "$HOME_DIR/.config/shell_init.d/10-sdkman.sh" \
  "$HOME_DIR/.config/shell_init.d/20_go.sh"; do
  check_exists "$f"
done

# Check for all installed binaries
for bin in starship sheldon fzf bat eza ripgrep zoxide direnv uv go; do
  check_bin "$bin"
done

# Check additional configuration files
for f in \
  "$HOME_DIR/.config/starship.toml" \
  "$HOME_DIR/.config/sheldon/plugins.toml"; do
  check_exists "$f"
done

# Check artifact cache
if [ -d "/tmp/terminal-ansible-artifacts" ]; then
  echo "[OK] Artifact cache present: /tmp/terminal-ansible-artifacts"
else
  echo "[FAIL] Artifact cache missing: /tmp/terminal-ansible-artifacts"
  failures=$((failures+1))
fi

# Check for shell sourcing
for shellrc in "$HOME_DIR/.bashrc" "$HOME_DIR/.zshrc" "$HOME_DIR/.profile"; do
  if grep -q 'shell_init.d' "$shellrc" 2>/dev/null; then
    echo "[OK] $shellrc sources shell_init.d"
  else
    echo "[FAIL] $shellrc does not source shell_init.d"
    failures=$((failures+1))
  fi
done

if [ "$failures" -eq 0 ]; then
  echo "[verify_appuser_terminal_env.sh] All checks passed."
  exit 0
else
  echo "[verify_appuser_terminal_env.sh] $failures check(s) failed."
  exit 1
fi
