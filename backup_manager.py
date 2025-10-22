import os
import shutil
from datetime import datetime
import json

class BackupManager:
    def __init__(self, backup_dir, max_files=10):
        self.backup_dir = backup_dir
        self.max_files = max_files
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, race_data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.json')
        
        with open(backup_file, 'w') as f:
            json.dump(race_data, f, indent=2)
        
        self._cleanup_old_backups()
    
    def _cleanup_old_backups(self):
        files = sorted(
            [f for f in os.listdir(self.backup_dir) if f.startswith('backup_')],
            key=lambda x: os.path.getctime(os.path.join(self.backup_dir, x))
        )
        
        while len(files) > self.max_files:
            os.remove(os.path.join(self.backup_dir, files.pop(0)))
