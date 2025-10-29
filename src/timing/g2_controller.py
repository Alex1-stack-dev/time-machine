"""
Enhanced Time Machine G2 Controller with full command set and error handling
"""
import serial
import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
from threading import Lock, Thread
from queue import Queue
import json

class G2Status(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"
    BUSY = "busy"
    READY = "ready"
    RACING = "racing"

class G2Error(Exception):
    """Base exception for G2 errors"""
    pass

class G2ConnectionError(G2Error):
    """Connection-related errors"""
    pass

class G2CommandError(G2Error):
    """Command execution errors"""
    pass

@dataclass
class G2Config:
    port: str = 'COM1'
    baudrate: int = 9600
    timeout: float = 1.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    heartbeat_interval: float = 5.0
    
@dataclass
class LaneTiming:
    lane: int
    time: float
    status: str
    splits: List[float]
    reaction_time: Optional[float] = None
    backup_times: List[float] = None

class G2Controller:
    def __init__(self, config: G2Config = G2Config()):
        self.config = config
        self.connection = None
        self.status = G2Status.DISCONNECTED
        self.lock = Lock()
        self.command_queue = Queue()
        self.last_error = None
        self.logger = logging.getLogger('G2Controller')
        
        # Start background workers
        self.heartbeat_thread = Thread(target=self._heartbeat_monitor, daemon=True)
        self.command_thread = Thread(target=self._command_processor, daemon=True)
        self.heartbeat_thread.start()
        self.command_thread.start()

    def connect(self) -> bool:
        """Establish connection with retry logic"""
        for attempt in range(self.config.retry_attempts):
            try:
                with self.lock:
                    self.connection = serial.Serial(
                        port=self.config.port,
                        baudrate=self.config.baudrate,
                        bytesize=8,
                        parity='N',
                        stopbits=1,
                        timeout=self.config.timeout
                    )
                    self.status = G2Status.CONNECTED
                    self._send_command('HELLO')  # Initial handshake
                    self.status = G2Status.READY
                    self.logger.info(f"Connected to G2 on {self.config.port}")
                    return True
            except serial.SerialException as e:
                self.last_error = str(e)
                self.logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(self.config.retry_delay)
        
        self.status = G2Status.ERROR
        raise G2ConnectionError(f"Failed to connect after {self.config.retry_attempts} attempts")

    def _send_command(self, cmd: str, expect_response: bool = True) -> Optional[str]:
        """Send command with error checking"""
        if self.status in [G2Status.DISCONNECTED, G2Status.ERROR]:
            raise G2ConnectionError("Not connected to G2")
            
        try:
            with self.lock:
                self.connection.write(f"{cmd}\r\n".encode())
                if expect_response:
                    response = self.connection.readline().decode().strip()
                    if response.startswith("ERROR"):
                        raise G2CommandError(f"G2 error: {response}")
                    return response
                return None
        except Exception as e:
            self.status = G2Status.ERROR
            self.last_error = str(e)
            raise G2CommandError(f"Command failed: {cmd} - {e}")

    def _heartbeat_monitor(self):
        """Monitor connection health"""
        while True:
            if self.status != G2Status.DISCONNECTED:
                try:
                    self._send_command('PING', expect_response=True)
                except Exception as e:
                    self.logger.error(f"Heartbeat failed: {e}")
                    self.status = G2Status.ERROR
            time.sleep(self.config.heartbeat_interval)

    def _command_processor(self):
        """Process commands from queue"""
        while True:
            cmd, args, callback = self.command_queue.get()
            try:
                result = getattr(self, cmd)(*args)
                if callback:
                    callback(result)
            except Exception as e:
                self.logger.error(f"Command processing error: {e}")
                if callback:
                    callback(None, error=str(e))

    # Enhanced G2 Commands
    
    def start_race(self, event: int, heat: int) -> bool:
        """Start race with full configuration"""
        try:
            self._send_command(f'EVENT {event}')
            self._send_command(f'HEAT {heat}')
            self._send_command('READY')
            time.sleep(0.5)  # Allow G2 to prepare
            self._send_command('START')
            self.status = G2Status.RACING
            return True
        except G2Error as e:
            self.logger.error(f"Race start failed: {e}")
            return False

    def stop_race(self) -> List[LaneTiming]:
        """Stop race and get results"""
        try:
            self._send_command('STOP')
            self.status = G2Status.READY
            return self.get_lane_times()
        except G2Error as e:
            self.logger.error(f"Race stop failed: {e}")
            return []

    def get_lane_times(self) -> List[LaneTiming]:
        """Get comprehensive lane timing data"""
        response = self._send_command('GET_TIMES')
        times = []
        
        for lane_data in response.split('|'):
            if not lane_data:
                continue
            try:
                parts = lane_data.split(',')
                times.append(LaneTiming(
                    lane=int(parts[0]),
                    time=float(parts[1]),
                    status=parts[2],
                    splits=[float(s) for s in parts[3].split(';')] if len(parts) > 3 else [],
                    reaction_time=float(parts[4]) if len(parts) > 4 else None,
                    backup_times=[float(t) for t in parts[5].split(';')] if len(parts) > 5 else None
                ))
            except (ValueError, IndexError) as e:
                self.logger.error(f"Error parsing lane data: {lane_data} - {e}")
                
        return times

    def get_splits(self, lane: int) -> List[float]:
        """Get split times for a specific lane"""
        response = self._send_command(f'GET_SPLITS {lane}')
        try:
            return [float(s) for s in response.split(',')]
        except ValueError as e:
            self.logger.error(f"Error parsing splits: {e}")
            return []

    def get_reaction_times(self) -> Dict[int, float]:
        """Get reaction times for all lanes"""
        response = self._send_command('GET_REACTION')
        times = {}
        try:
            for lane_data in response.split('|'):
                if lane_data:
                    lane, time = lane_data.split(',')
                    times[int(lane)] = float(time)
            return times
        except ValueError as e:
            self.logger.error(f"Error parsing reaction times: {e}")
            return {}

    def set_lane_status(self, lane: int, status: str) -> bool:
        """Set lane status (DQ, scratch, etc.)"""
        try:
            self._send_command(f'SET_STATUS {lane} {status}')
            return True
        except G2Error:
            return False

    def backup_times(self, lane: int, times: List[float]) -> bool:
        """Add backup times for a lane"""
        times_str = ';'.join(str(t) for t in times)
        try:
            self._send_command(f'BACKUP {lane} {times_str}')
            return True
        except G2Error:
            return False

    def configure_timing(self, **kwargs) -> bool:
        """Configure timing parameters"""
        config_str = json.dumps(kwargs)
        try:
            self._send_command(f'CONFIG {config_str}')
            return True
        except G2Error:
            return False

    def get_diagnostics(self) -> Dict:
        """Get system diagnostic information"""
        try:
            response = self._send_command('DIAG')
            return json.loads(response)
        except Exception as e:
            self.logger.error(f"Diagnostics failed: {e}")
            return {}
