# cx_Freeze setup script to produce a Windows executable for main.py
from cx_Freeze import setup, Executable
import os
import sys

ENTRY_SCRIPT = "main.py"
TARGET_NAME = "time-machine.exe"

include_files = []
if os.path.isdir("public"):
    include_files.append(("public", "public"))

build_exe_options = {
    "packages": ["os", "sys", "threading", "uvicorn", "fastapi", "pydantic"],
    "includes": [],
    "excludes": [],
    "include_files": include_files,
}

base = None
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
