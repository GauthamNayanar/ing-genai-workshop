#!/usr/bin/env bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

venv_dir=".venv"
requirements_file="requirements.txt"
venv_python="$venv_dir/bin/python"

echo "[1/3] Checking uv installation..."
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Installing uv via curl..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[2/3] Preparing virtual environment '$venv_dir'..."
if [ ! -d "$venv_dir" ]; then
  uv venv "$venv_dir"
else
  echo "Reusing existing virtual environment '$venv_dir'."
fi

echo "[3/3] Installing requirements from '$requirements_file'..."
uv pip install --python "$venv_python" -r "$requirements_file"

echo "Virtual environment setup complete. Activate it with: source $venv_dir/bin/activate"
