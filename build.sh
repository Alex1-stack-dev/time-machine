#!/usr/bin/env bash
set -euo pipefail

# Unix / macOS build script
# - creates a virtualenv
# - installs requirements
# - runs pyinstaller with the included spec

VENV_DIR=.venv-build

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Build single-file executable
pyinstaller --clean --noconfirm raceclock.spec

echo "Build complete. Dist folder contains your app (dist/time-machine)."
