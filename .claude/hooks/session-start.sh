#!/bin/bash
# Installs project dependencies in Claude Code cloud sessions so that
# `make lint` (mypy, flake8 + wemake-python-styleguide) and the formatters work right away.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

export PATH="$HOME/.local/bin:$PATH"

if ! command -v poetry >/dev/null 2>&1; then
  if command -v uv >/dev/null 2>&1; then
    uv tool install poetry
  elif command -v pipx >/dev/null 2>&1; then
    pipx install poetry
  else
    python3 -m pip install --user poetry
  fi
fi

# Idempotent: poetry only installs what is missing from the lock file.
# Dev group (mypy, flake8, wemake-python-styleguide, black, isort) is included.
poetry install --no-interaction -E all

# `make lint` relies on the wemake-python-styleguide flake8 plugin.
poetry run python -c "import wemake_python_styleguide"

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
