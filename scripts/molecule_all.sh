#!/usr/bin/env bash
set -euo pipefail

# Environment variables:
#   COLIMA_SOCKET - Optional path to a custom Docker socket. If set, DOCKER_HOST
#     will be configured to use this socket.

if [ -n "${COLIMA_SOCKET:-}" ]; then
  export DOCKER_HOST="unix://$COLIMA_SOCKET"
fi

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
