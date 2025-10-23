# cx_Freeze setup script to produce a Windows executable for main.py
# Usage (local): python setup_cx_freeze.py build
# The workflow uses the same command in CI.
import sys
from cx_Freeze import setup, Executable
import os

# Adjust these if your entry point or static path is different
ENTRY_SCRIPT = "main.py"
TARGET_NAME = "time-machine.exe"

# Include static public files and other data (preserve directory structure)
include_files = []
if os.path.isdir("public"):
    include_files.append(("public", "public"))

build_exe_options = {
    "packages": ["os", "sys", "threading", "uvicorn", "fastapi", "pydantic"],
    "includes": [],
    "excludes": [],
    "include_files": include_files,
    # You can tune optimization and compression options here
}

base = None
# Use GUI base to hide console. If you want a console window for logs, set base = None
# On Windows use "Win32GUI" to suppress console window for GUI apps
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(ENTRY_SCRIPT, base=base, target_name=TARGET_NAME),
]

setup(
    name="time-machine",
    version="1.0.0",
    description="Time Machine desktop application",
    options={"build_exe": build_exe_options},
    executables=executables,
)
