# Build instructions — Time Machine desktop app

This document explains how to build a single-file executable of the Time Machine app for local desktop use.

Prerequisites
- Python 3.8+ installed
- On Windows: Visual C++ Build Tools for some wheels (if compilation required)
- On macOS/Linux: standard dev tools as needed
- requirements.txt present and accurate (must include: fastapi, uvicorn, pydantic; add pyqt5 if you later implement GUI)

Quick steps (Unix / macOS)
1. Add the files in this PR to your repository.
2. Run:
   ```
   ./build.sh
   ```
3. Result: `dist/time-machine` (or similar) — test by running it locally:
   ```
   ./dist/time-machine
   ```

Quick steps (Windows)
1. Add the files to the repo.
2. Run `build_windows.bat` from cmd.exe.
3. Result: `dist\time-machine\time-machine.exe`.

Run without packaging (development)
1. Create a venv and install requirements:
   ```
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install uvicorn
   ```
2. Run the launcher:
   ```
   python main.py
   ```
   The launcher starts the local server and opens the UI in your browser at http://127.0.0.1:8000/meet.html

Notes and next steps
- Persistence: this prototype stores meet state in memory. Add a DB (SQLite/Postgres) if you want persistent meet data between runs.
- Hardware interface: you cannot access USB/serial from Vercel. Run hardware gateway code on the machine with the serial device and forward events to this local server or persist them to the shared DB.
- Packaging improvements:
  - For macOS consider creating a .app bundle (use py2app or PyInstaller one-dir and macOS bundler).
  - For Windows create an installer (NSIS/Inno Setup) that places the exe and shortcuts.
- If you want a native PyQt GUI instead of a browser UI, I can scaffold a small PyQt main window that talks to the same local server or integrates logic directly.
