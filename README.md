```markdown
# Time Machine — Windows GUI (Hy‑Tek style)

Time Machine is a desktop application packaged as a Windows .exe. This repository contains the source, an auto-update mechanism, and CI to build Windows executables.

Key features
- Hy‑Tek-like UI for managing meets/events (left list + main grid).
- Splash image on startup.
- Auto-update: app checks GitHub Releases; downloads and applies updates automatically without asking users to manually reinstall.
- CI: builds Windows .exe and updater.exe when you push a tag (vMAJOR.MINOR.PATCH).

Quick start (developer)
1. Install dependencies (for development)
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Run app (dev)
   python -m src.main

Releasing (host)
1. Bump VERSION in src/main.py.
2. Tag and push:
   git tag vX.Y.Z
   git push origin vX.Y.Z
3. The GitHub Actions workflow `.github/workflows/release-windows.yml` will:
   - Build `time-machine.exe` and `time-machine-updater.exe` with PyInstaller
   - Compute SHA256
   - Create a GitHub Release and upload the assets

Auto-update behavior (user)
- App checks Releases and downloads new exe + .sha256.
- Verifies the downloaded exe with SHA256.
- Launches updater helper to replace the running exe and restart it.

Notes and recommendations
- Code-sign builds to reduce SmartScreen warnings.
- Host your releases on GitHub Releases (the workflow does this automatically when you push a tag).
- If you install app to Program Files, the updater will require elevation — prefer installing in per-user location (e.g., %LOCALAPPDATA%).

See docs/ for more details.
```
