#!/usr/bin/env bash
set -euo pipefail


# Run ansible-lint on all roles and collection root
find "$(dirname "$0")/.." \
  -type f \
  \( -name '*.yml' -o -name '*.yaml' \) \
  ! -path '*/.venv/*' \
  ! -path '*/site-packages/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/.mypy_cache/*' \
  ! -path '*/molecule/*/verify.yml' \
  ! -path '*/molecule/*/converge.yml' \
  -exec ansible-lint {} +

echo "Ansible Lint completed successfully."
