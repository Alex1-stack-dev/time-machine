@echo off
REM Windows build script (run from project root in cmd.exe)
REM Requires Python 3.8+ and pip available

python -m venv .venv-build
call .venv-build\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --clean --noconfirm raceclock.spec

echo Build complete. Check dist\time-machine
pause
