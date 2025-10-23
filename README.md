```markdown
# Time Machine — Quick Start (very simple)

This repo contains a local desktop-style app that runs a small web UI and a local server to control/record meet events.

Before you start:
- Copy `.env.example` to `.env` and set `API_KEY` to a long random string.
- Keep `.env` private (do not commit it).

How to run this on your computer (easy / like I'm 5)

1) Get the code:
- Click "Code" on GitHub → "Download ZIP" or run:
  - git clone https://github.com/<your-user>/time-machine.git
  - cd time-machine

2) Make a little private space for the app (virtualenv):
- On macOS / Linux:
  - python3 -m venv .venv
  - source .venv/bin/activate
- On Windows (PowerShell):
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1

3) Tell pip to get the right pieces:
- pip install --upgrade pip
- pip install -r requirements.txt

4) Make a private file with your secret key:
- Copy .env.example to .env, then edit .env
  - On macOS / Linux: cp .env.example .env && nano .env
  - On Windows (PowerShell): copy .env.example .env; notepad .env
- Put a long random string for API_KEY (keeps admin actions safe)

5) Start the app (the launcher starts a local server and opens a browser):
- python main.py
- A browser window/tab should open at: http://127.0.0.1:8000/meet.html

6) If you prefer to run server directly:
- uvicorn server:app --host 127.0.0.1 --port 8000 --reload
- Then open: http://127.0.0.1:8000/meet.html

What the UI does (simple)
- Add runners (Entries)
- Start / Stop meet
- Record finishes
- View events and results

If you make changes and want to build a Windows .exe (optional)
- I included a GitHub Actions workflow that builds a Windows bundle (cx_Freeze) and uploads it as a zip artifact.
- Or build locally on Windows using `windows_local_build.bat` or `setup_cx_freeze.py`.

Safety tips before using on real hardware
- Test in a spare machine or VM first.
- Make sure serial drivers for your raceclock are installed.
- Use a strong API_KEY and do not expose the app to the public Internet without TLS and proper auth.
```
