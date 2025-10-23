#!/bin/bash
# Example systemd service wrapper to run the packaged app in background
# Put this script on Linux host and create a systemd unit to call it (see README_SECURITY.md)

VENV_DIR=/opt/time-machine/.venv
APP_DIR=/opt/time-machine
USER=youruser

# activate venv if exists
if [ -f "${VENV_DIR}/bin/activate" ]; then
  source "${VENV_DIR}/bin/activate"
fi

cd "${APP_DIR}"
# run the launcher (main.py) under the user account
exec /usr/bin/env python main.py
