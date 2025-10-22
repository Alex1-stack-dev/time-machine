import serial
import serial.tools.list_ports

class SerialManager:
    def __init__(self):
        self.ser = None
        self.connected = False

    def list_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port, baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=0.1)
            self.connected = True
        except Exception as e:
            self.connected = False
            print(f"Serial connection error: {e}")

    def disconnect(self):
        if self.ser and self.connected:
            self.ser.close()
            self.connected = False

    def send_command(self, cmd):
        if self.ser and self.connected:
            self.ser.write((cmd + '\r\n').encode('ascii'))

    def read_line(self):
        if self.ser and self.connected:
            try:
                if self.ser.in_waiting:
                    return self.ser.readline().decode('ascii').strip()
            except Exception as e:
                print(f"Serial read error: {e}")
        return ''
