import os
import shutil
from datetime import datetime
import sqlite3
import logging

logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, backup_dir="backups", max_files=10, db_path="data/time_machine.db"):
        self.backup_dir = backup_dir
        self.max_files = max_files
        self.db_path = db_path
        os.makedirs(backup_dir, exist_ok=True)

    def create_backup(self):
        if not os.path.exists(self.db_path):
            logger.warning("No DB to backup at %s", self.db_path)
            return None
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'time_machine_{timestamp}.db')
        try:
            # Use sqlite backup to ensure file integrity
            dest_conn = sqlite3.connect(backup_file)
            src_conn = sqlite3.connect(self.db_path)
            with dest_conn:
                src_conn.backup(dest_conn)
            dest_conn.close()
            src_conn.close()
            logger.info("Created DB backup %s", backup_file)
            self._cleanup_old_backups()
            return backup_file
        except Exception as e:
            logger.exception("Failed to create DB backup: %s", e)
            return None

    def _cleanup_old_backups(self):
        files = sorted(
            [f for f in os.listdir(self.backup_dir) if f.endswith('.db')],
            key=lambda x: os.path.getctime(os.path.join(self.backup_dir, x))
        )
        while len(files) > self.max_files:
            old = files.pop(0)
            try:
                os.remove(os.path.join(self.backup_dir, old))
                logger.info("Removed old backup %s", old)
            except Exception:
                logger.exception("Failed to remove old backup %s", old)
            os.remove(os.path.join(self.backup_dir, files.pop(0)))
