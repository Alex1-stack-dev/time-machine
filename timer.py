from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer
from core.serial_manager import SerialManager
from core.protocol import TimeMachineG2Protocol

class TimerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.protocol = TimeMachineG2Protocol()
        self.serial_mgr = SerialManager()
        self.current_time = "00:00.00"
        self.is_running = False
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_serial)
        self.timer.start(100)

    def init_ui(self):
        layout = QVBoxLayout()
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.refresh_ports()
        port_layout.addWidget(QLabel("Serial Port:"))
        port_layout.addWidget(self.port_combo)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.handle_connect)
        port_layout.addWidget(self.connect_btn)
        layout.addLayout(port_layout)

        timer_layout = QHBoxLayout()
        self.timer_label = QLabel("00:00.00")
        self.timer_label.setStyleSheet("font-size: 36pt;")
        timer_layout.addWidget(self.timer_label)
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(lambda: self.send_cmd('START'))
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(lambda: self.send_cmd('STOP'))
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(lambda: self.send_cmd('RESET'))
        self.split_btn = QPushButton("Split/Lap")
        self.split_btn.clicked.connect(lambda: self.send_cmd('SPLIT'))
        for btn in [self.start_btn, self.stop_btn, self.reset_btn, self.split_btn]:
            timer_layout.addWidget(btn)
        layout.addLayout(timer_layout)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
        self.setLayout(layout)

    def refresh_ports(self):
        ports = self.serial_mgr.list_ports()
        self.port_combo.clear()
        self.port_combo.addItems(ports)

    def handle_connect(self):
        port = self.port_combo.currentText()
        if not self.serial_mgr.connected:
            self.serial_mgr.connect(port)
            if self.serial_mgr.connected:
                self.connect_btn.setText("Disconnect")
                self.log.append(f"Connected to {port}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to connect to {port}")
        else:
            self.serial_mgr.disconnect()
            self.connect_btn.setText("Connect")
            self.log.append("Disconnected")

    def send_cmd(self, action):
        cmd = self.protocol.build_command(action)
        self.serial_mgr.send_command(cmd)
        self.log.append(f"Sent command: {action}")

    def poll_serial(self):
        line = self.serial_mgr.read_line()
        if line:
            parsed = self.protocol.parse_response(line)
            if parsed["type"] == "time":
                self.current_time = parsed["value"]
                self.timer_label.setText(self.current_time)
            self.log.append(f"{parsed['type'].capitalize()}: {parsed['value']}")
