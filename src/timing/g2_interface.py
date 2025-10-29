"""
Time Machine G2 Race Clock Interface
Handles communication with Electro-numerics Time Machine G2 via RS232/USB
"""
import serial
import time
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LaneTiming:
    lane: int
    time: float
    status: str  # 'valid', 'dq', 'scratch'

class G2Interface:
    def __init__(self, port: str = 'COM1', baudrate: int = 9600):
        """Initialize connection to Time Machine G2"""
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish connection to G2 device"""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            self.connected = True
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to G2: {e}")
            return False

    def get_lane_times(self) -> List[LaneTiming]:
        """Read current lane times from G2"""
        if not self.connected:
            return []
            
        try:
            # Send request for lane times
            self.connection.write(b'GET_TIMES\r\n')
            
            # Read response
            response = self.connection.readline().decode().strip()
            
            # Parse lane times
            # Format: LANE,TIME,STATUS|LANE,TIME,STATUS|...
            times = []
            for lane_data in response.split('|'):
                if not lane_data:
                    continue
                lane, time, status = lane_data.split(',')
                times.append(LaneTiming(
                    lane=int(lane),
                    time=float(time),
                    status=status
                ))
            
            return times
            
        except Exception as e:
            print(f"Error reading from G2: {e}")
            return []

    def start_race(self):
        """Send start signal to G2"""
        if self.connected:
            self.connection.write(b'START\r\n')

    def stop_race(self):
        """Send stop signal to G2"""
        if self.connected:
            self.connection.write(b'STOP\r\n')

    def reset_timer(self):
        """Reset G2 timer"""
        if self.connected:
            self.connection.write(b'RESET\r\n')

    def set_event(self, event_number: int):
        """Set current event number on G2"""
        if self.connected:
            self.connection.write(f'EVENT {event_number}\r\n'.encode())

    def set_heat(self, heat_number: int):
        """Set current heat number on G2"""
        if self.connected:
            self.connection.write(f'HEAT {heat_number}\r\n'.encode())
