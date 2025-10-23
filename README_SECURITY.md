```markdown
# Security & Reliability Checklist — Time Machine

This file documents the security and hardening measures added to the repository and the recommended steps before using the app in production.

What we added
- SQLite persistence so state survives restarts.
- API key (x-api-key) authentication for admin endpoints (add entry, start/stop, record event).
- CORS restricted to localhost origins by default.
- Rotating file logging to logs/app.log.
- DB backup manager that snapshots the database on important actions.
- CI workflow that runs unit tests and security checks (Bandit, pip-audit, safety).

Before you run the app on a production machine
1. Set a secure API key:
   - Copy `.env.example` to `.env` and set a long random value for API_KEY.
   - Ensure `.env` is not committed to Git if it will contain secrets.

2. Run initial tests locally:
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt
   - pytest

3. Validate drivers & hardware:
   - Ensure serial/USB drivers for your raceclock are installed and working on the target OS.
   - Test hardware integration on a spare machine first.

4. Run in a sandbox for the first run:
   - Use a VM or disposable machine to validate connectivity and behavior.

5. Tighten access before exposing remotely:
   - Do not expose the app directly to the public Internet without TLS, authentication, and rate limiting.
   - Consider adding a reverse proxy (nginx) and HTTP Basic or token auth in front if needed.

6. Backups and monitoring:
   - Ensure the `backups/` folder is backed up regularly.
   - Add health probes and a supervisor to restart the process on failure.

CI & Security scan notes
- The repository contains a GitHub Actions workflow that runs static and dependency checks; always inspect test and security logs before trusting a CI artifact.
- Pin versions in requirements.txt to reduce supply-chain risk and run `pip-audit` and `safety` on dependencies regularly.

If you want, I can:
- Add token rotation and expiry, or integrate with a local user/password login (SQLite users table).
- Add TLS and a reverse-proxy example.
- Create a systemd unit and Windows service installer example to run the app as a supervised service.
```
