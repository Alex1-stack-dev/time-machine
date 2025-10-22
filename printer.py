import serial

class ThermalPrinter:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=1)

    def print_text(self, text):
        # ESC/POS or device-specific protocol if needed
        self.ser.write(text.encode('ascii'))
        self.ser.flush()

    def print_results(self, results):
        for r in results:
            self.print_text(f"{r.place}. {r.name} {r.time} Heat: {r.heat} {'DQ' if r.dq else ''}\n")
