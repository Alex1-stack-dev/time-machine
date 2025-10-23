#!/usr/bin/env python3
"""
Launcher for the Time Machine desktop app.

- Starts the local FastAPI server (server.app) in a background thread.
- Opens the user's default browser to the local UI.
- Keeps the process alive while the server runs.
"""
import threading
import time
import webbrowser
import socket
import sys

def wait_for_port(host: str, port: int, timeout: float = 5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except Exception:
            time.sleep(0.1)
    return False

def start_server():
    # Import here so PyInstaller bundles server.py properly
    import server
    import uvicorn
    # run uvicorn programmatically; this blocks so we run it in a thread
    uvicorn.run(server.app, host="127.0.0.1", port=8000, log_level="info")

def main():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

    # Wait for server to be ready
    if not wait_for_port("127.0.0.1", 8000, timeout=8.0):
        print("Server didn't start within timeout. Check logs.", file=sys.stderr)
        sys.exit(1)

    url = "http://127.0.0.1:8000/meet.html"
    print("Opening UI at", url)
    webbrowser.open(url)

    try:
        # Keep running until user exits (Ctrl+C)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
