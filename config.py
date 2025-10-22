import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Serial Communication
    SERIAL_BAUDRATE = int(os.getenv('SERIAL_BAUDRATE', '9600'))
    SERIAL_TIMEOUT = float(os.getenv('SERIAL_TIMEOUT', '1.0'))
    
    # Application Settings
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'raceclock.log')
    
    # Data Export Settings
    BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
    MAX_BACKUP_FILES = int(os.getenv('MAX_BACKUP_FILES', '10'))
    
    # Database Settings
    DB_PATH = os.getenv('DB_PATH', 'race_data.db')
