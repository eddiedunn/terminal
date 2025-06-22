#!/usr/bin/env bash
set -euo pipefail

# Activate UV virtualenv if present
if [ -f "$(dirname "$0")/../.venv/bin/activate" ]; then
  source "$(dirname "$0")/../.venv/bin/activate"
fi

# Run ansible-lint on all roles and collection root
find "$(dirname "$0")/.." \
  -type f \
  \( -name '*.yml' -o -name '*.yaml' \) \
  ! -path '*/molecule/*/verify.yml' \
  ! -path '*/molecule/*/converge.yml' \
  -exec ansible-lint {} +

echo "Ansible Lint completed successfully."
