"""
Enhanced error handling for G2 timing system
"""
from typing import Optional, Dict, List
import logging
from enum import Enum
from datetime import datetime

class G2ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class G2ErrorCode(Enum):
    # Connection errors
    CONN_FAILED = "E001"
    CONN_LOST = "E002"
    CONN_TIMEOUT = "E003"
    
    # Command errors
    CMD_INVALID = "E101"
    CMD_TIMEOUT = "E102"
    CMD_REJECTED = "E103"
    
    # Hardware errors
    PAD_FAILURE = "E201"
    STARTER_FAILURE = "E202"
    BATTERY_LOW = "E203"
    
    # Timing errors
    TIME_INVALID = "E301"
    TIME_MISSING = "E302"
    SPLITS_INVALID = "E303"
    
    # System errors
    SYS_MEMORY = "E901"
    SYS_CONFIG = "E902"
    SYS_STATE = "E903"

class G2Error(Exception):
    def __init__(self, 
                 code: G2ErrorCode,
                 message: str,
                 severity: G2ErrorSeverity = G2ErrorSeverity.ERROR,
                 timestamp: Optional[datetime] = None,
                 details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.severity = severity
        self.timestamp = timestamp or datetime.utcnow()
        self.details = details or {}
        super().__init__(f"{code.value}: {message}")

class G2ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger('G2ErrorHandler')
        self.error_history: List[G2Error] = []
        self.max_history = 1000
        
    def handle_error(self, error: G2Error) -> bool:
        """Handle G2 error and return whether it's recoverable"""
        self.error_history.append(error)
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)
            
        self.logger.log(
            logging.ERROR if error.severity in [G2ErrorSeverity.ERROR, G2ErrorSeverity.CRITICAL] else logging.WARNING,
            f"G2 Error: [{error.code.value}] {error.message}"
        )
        
        # Determine if error is recoverable
        recoverable = error.code.value not in ['E201', 'E202', 'E901']
        
        if error.severity == G2ErrorSeverity.CRITICAL:
            self.trigger_emergency_shutdown()
            
        return recoverable
        
    def get_recent_errors(self, 
                         severity: Optional[G2ErrorSeverity] = None,
                         limit: int = 10) -> List[G2Error]:
        """Get recent errors, optionally filtered by severity"""
        errors = self.error_history
        if severity:
            errors = [e for e in errors if e.severity == severity]
        return sorted(errors, key=lambda e: e.timestamp, reverse=True)[:limit]
        
    def clear_history(self):
        """Clear error history"""
        self.error_history.clear()
        
    def trigger_emergency_shutdown(self):
        """Handle critical errors with emergency shutdown"""
        self.logger.critical("Emergency shutdown triggered")
        # Implement emergency shutdown logic
