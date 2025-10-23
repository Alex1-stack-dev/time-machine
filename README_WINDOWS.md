```markdown
# Building a Windows executable (no PyInstaller) — Time Machine

This guide explains how to get a downloadable .exe produced automatically via GitHub Actions, or how to build locally with cx_Freeze.

Do I need to delete repo files?
- No. Keep your repo as-is. Add the files:
  - .github/workflows/build-windows.yml
  - setup_cx_freeze.py
  - windows_local_build.bat
  - (and keep your existing main.py, server.py, public/ etc.)
- The workflow builds the .exe without deleting or changing other files.

How the GitHub Actions flow works
- When you push to `main` (or trigger the workflow manually), Actions will:
  - set up a Windows runner,
  - install dependencies (from requirements.txt) plus cx-Freeze,
  - run `python setup_cx_freeze.py build`,
  - zip the build folder and upload a downloadable artifact named `time-machine-windows`.

Where to download the .exe
- Go to your repository -> Actions -> select the latest workflow run -> Artifacts -> time-machine-windows -> download the zip. Inside will be the built binary and supporting files.

Notes and caveats
- cx_Freeze bundles Python and your resources; the produced folder is usually under `build\exe.win-amd64-*` (cx_Freeze build naming varies by Python version). The workflow zips the full build directory.
- The produced bundle may be flagged by antivirus until you code-sign it. Consider signing the executable if you distribute to others.
- If your app depends on system-level components (e.g., PyQt5 or compiled C extensions), the Windows runner may require additional dependencies. Test the artifact thoroughly.
- For a one-click installer: add NSIS or Inno Setup steps in the workflow to create an installer (.exe or .msi) and upload it as an artifact or create a GitHub Release.

If you want, next I can:
- add a workflow step that automatically creates a GitHub Release and attaches the built .zip,
- or change the build to use Nuitka (smaller/faster binary) or create an installer with NSIS,
- or adapt the build steps to produce a portable single exe vs. an exe+supporting files bundle.
