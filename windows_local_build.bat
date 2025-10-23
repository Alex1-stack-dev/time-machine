@echo off
REM Local Windows build script using cx_Freeze
REM Run this from project root on a Windows machine with Python installed

python -m venv .venv-build
call .venv-build\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install cx-Freeze==6.14

REM Build
python setup_cx_freeze.py build

if exist build (
  echo Build produced 'build' directory. You can find the exe under build\*
) else (
  echo Build failed. Check the console output for errors.
)
pause
