#!/usr/bin/env bash
set -euo pipefail


# Use the Colima Docker socket if available
export DOCKER_HOST=${DOCKER_HOST:-"unix://$HOME/.colima/docker.sock"}

# Activate the Python venv for ansible/molecule
source "$(dirname "$0")/../../.venv/bin/activate"

ROOT=$(dirname $(dirname $(realpath "$0")))
ROLES=(env_chassis nvm pyenv rustup profile)
FAIL=0

for role in "${ROLES[@]}"; do
  echo "=== Running molecule test for $role ==="
  cd "$ROOT/roles/$role"
  if ! molecule test --destroy=always; then
    echo "[FAIL] Molecule test failed for $role"
    FAIL=1
  fi
  cd - >/dev/null
  echo
  echo "=============================="
done

if [[ $FAIL -eq 0 ]]; then
  echo "All Molecule tests passed."
  exit 0
else
  echo "Some Molecule tests failed."
  exit 1
fi
