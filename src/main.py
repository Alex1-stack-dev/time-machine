# This part already exists in the code - it checks for updates on startup
def check_for_updates(parent_window=None, show_result=True):
    """
    Check GitHub Releases for a newer version.
    Downloads and installs update if available.
    """
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        latest = r.json()
        
        # Compare versions
        if Version(latest["tag_name"].lstrip("v")) > Version(VERSION):
            # Download new version
            download_url = latest["assets"][0]["browser_download_url"]
            
            # Download and verify
            update_dir = Path(os.getenv("LOCALAPPDATA")) / "TimeMachine" / "updates"
            update_dir.mkdir(parents=True, exist_ok=True)
            new_exe = update_dir / "time-machine-new.exe"
            
            # Download
            with requests.get(download_url, stream=True) as r:
                with open(new_exe, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
            
            # Launch updater to replace exe
            updater_path = get_local_exe_path().parent / "time-machine-updater.exe"
            if updater_path.exists():
                subprocess.Popen([
                    str(updater_path),
                    "--target", str(get_local_exe_path()),
                    "--new", str(new_exe),
                    "--restart"
                ])
                QtWidgets.QApplication.quit()
                return True
                
    except Exception as e:
        if show_result:
            QtWidgets.QMessageBox.warning(parent_window, "Update Error", str(e))
    return False

# Add these lines to enable automatic update checks
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # ... existing init code ...
        
        # Check for updates every hour
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(lambda: check_for_updates(self, show_result=False))
        self.update_timer.start(3600000)  # 1 hour in milliseconds
        
        # Also check at startup
        QtCore.QTimer.singleShot(5000, lambda: check_for_updates(self, show_result=False))
