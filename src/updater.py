#!/usr/bin/env python3
"""
Updater helper.
Usage:
    updater.exe --target "C:\path\time-machine.exe" --new "C:\path\time-machine-new.exe" --restart

Behavior:
- Wait for the target process to exit (by path)
- Replace the target file atomically
- Optionally restart the target
"""
import argparse
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

def is_process_running(path):
    # Try to find processes with this executable path (Windows only)
    try:
        import psutil
    except ImportError:
        return False
    for p in psutil.process_iter(["exe"]):
        try:
            exe = p.info.get("exe")
            if exe and Path(exe).resolve() == Path(path).resolve():
                return True
        except Exception:
            continue
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Path to the running exe to replace")
    parser.add_argument("--new", required=True, help="Path to the new exe to move into place")
    parser.add_argument("--restart", action="store_true", help="Restart the replaced app")
    parser.add_argument("--timeout", type=int, default=30, help="Seconds to wait for target to exit")
    args = parser.parse_args()

    target = Path(args.target)
    new = Path(args.new)

    # Wait for the target to be free
    timeout = args.timeout
    elapsed = 0
    while elapsed < timeout:
        if not is_process_running(target):
            break
        time.sleep(0.5)
        elapsed += 0.5

    # If still running, attempt to continue anyway
    try:
        # make a backup
        backup = target.with_suffix(".bak")
        if target.exists():
            try:
                target.replace(backup)
            except Exception:
                try:
                    target.unlink()
                except Exception:
                    pass
        # move new into place
        new.replace(target)
        # cleanup backup
        if backup.exists():
            backup.unlink()
    except Exception as e:
        print("Updater error:", e)
        sys.exit(2)

    if args.restart:
        try:
            subprocess.Popen([str(target)], close_fds=True)
        except Exception as e:
            print("Failed to restart:", e)

    sys.exit(0)

if __name__ == "__main__":
    main()
