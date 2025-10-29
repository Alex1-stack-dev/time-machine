"""
Time Machine G2 Control Panel GUI
"""
from PySide6 import QtWidgets, QtCore, QtGui
from ..timing.g2_controller import G2Controller, G2Status, G2Config
from typing import Optional, Callable
import json

class G2ControlPanel(QtWidgets.QWidget):
    statusChanged = QtCore.Signal(str)
    raceStarted = QtCore.Signal()
    raceStopped = QtCore.Signal(list)  # List[LaneTiming]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.g2 = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # Connection group
        conn_group = QtWidgets.QGroupBox("G2 Connection")
        conn_layout = QtWidgets.QHBoxLayout()
        
        self.port_combo = QtWidgets.QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3', 'COM4'])
        
        self.connect_btn = QtWidgets.QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        
        self.status_label = QtWidgets.QLabel("Disconnected")
        
        conn_layout.addWidget(QtWidgets.QLabel("Port:"))
        conn_layout.addWidget(self.port_combo)
        conn_layout.addWidget(self.connect_btn)
        conn_layout.addWidget(self.status_label)
        conn_group.setLayout(conn_layout)
        
        # Race control group
        race_group = QtWidgets.QGroupBox("Race Control")
        race_layout = QtWidgets.QGridLayout()
        
        self.event_spin = QtWidgets.QSpinBox()
        self.event_spin.setRange(1, 999)
        
        self.heat_spin = QtWidgets.QSpinBox()
        self.heat_spin.setRange(1, 99)
        
        self.start_btn = QtWidgets.QPushButton("Start Race")
        self.start_btn.clicked.connect(self.start_race)
        self.start_btn.setEnabled(False)
        
        self.stop_btn = QtWidgets.QPushButton("Stop Race")
        self.stop_btn.clicked.connect(self.stop_race)
        self.stop_btn.setEnabled(False)
        
        race_layout.addWidget(QtWidgets.QLabel("Event:"), 0, 0)
        race_layout.addWidget(self.event_spin, 0, 1)
        race_layout.addWidget(QtWidgets.QLabel("Heat:"), 0, 2)
        race_layout.addWidget(self.heat_spin, 0, 3)
        race_layout.addWidget(self.start_btn, 1, 0, 1, 2)
        race_layout.addWidget(self.stop_btn, 1, 2, 1, 2)
        race_group.setLayout(race_layout)
        
        # Times display
        times_group = QtWidgets.QGroupBox("Lane Times")
        times_layout = QtWidgets.QVBoxLayout()
        
        self.times_table = QtWidgets.QTableWidget(8, 4)
        self.times_table.setHorizontalHeaderLabels(
            ["Lane", "Time", "Splits", "Status"])
        
        times_layout.addWidget(self.times_table)
        times_group.setLayout(times_layout)
        
        # Diagnostics group
        diag_group = QtWidgets.QGroupBox("Diagnostics")
        diag_layout = QtWidgets.QVBoxLayout()
        
        self.diag_text = QtWidgets.QTextEdit()
        self.diag_text.setReadOnly(True)
        
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_diagnostics)
        
        diag_layout.addWidget(self.diag_text)
        diag_layout.addWidget(self.refresh_btn)
        diag_group.setLayout(diag_layout)
        
        # Add all groups to main layout
        layout.addWidget(conn_group)
        layout.addWidget(race_group)
        layout.addWidget(times_group)
        layout.addWidget(diag_group)
        
        # Status bar
        self.status_bar = QtWidgets.QStatusBar()
        layout.addWidget(self.status_bar)
        
        # Setup update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_times)
        self.update_timer.setInterval(100)  # 100ms updates
        
    def toggle_connection(self):
        if not self.g2 or self.g2.status == G2Status.DISCONNECTED:
            self.connect_g2()
        else:
            self.disconnect_g2()
            
    def connect_g2(self):
        try:
            config = G2Config(port=self.port_combo.currentText())
            self.g2 = G2Controller(config)
            self.g2.connect()
            
            self.connect_btn.setText("Disconnect")
            self.start_btn.setEnabled(True)
            self.update_timer.start()
            
            self.status_bar.showMessage("Connected to G2")
            self.statusChanged.emit("connected")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Connection Error",
                f"Failed to connect to G2: {str(e)}"
            )
            
    def disconnect_g2(self):
        if self.g2:
            self.update_timer.stop()
            self.g2 = None
            
        self.connect_btn.setText("Connect")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status_bar.showMessage("Disconnected")
        self.statusChanged.emit("disconnected")
        
    def start_race(self):
        if not self.g2:
            return
            
        try:
            event = self.event_spin.value()
            heat = self.heat_spin.value()
            
            if self.g2.start_race(event, heat):
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
                self.status_bar.showMessage("Race in progress")
                self.raceStarted.emit()
            else:
                raise Exception("Failed to start race")
                
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Race Start Error",
                f"Failed to start race: {str(e)}"
            )
            
    def stop_race(self):
        if not self.g2:
            return
            
        try:
            times = self.g2.stop_race()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_bar.showMessage("Race completed")
            self.raceStopped.emit(times)
            self.update_times_display(times)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Race Stop Error",
                f"Failed to stop race: {str(e)}"
            )
            
    def update_times(self):
        if not self.g2 or self.g2.status != G2Status.RACING:
            return
            
        try:
            times = self.g2.get_lane_times()
            self.update_times_display(times)
        except Exception as e:
            self.status_bar.showMessage(f"Error updating times: {str(e)}")
            
    def update_times_display(self, times):
        self.times_table.setRowCount(len(times))
        for i, time in enumerate(times):
            self.times_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(time.lane)))
            self.times_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{time.time:.2f}"))
            self.times_table.setItem(i, 2, QtWidgets.QTableWidgetItem(
                ", ".join(f"{s:.2f}" for s in time.splits)))
            self.times_table.setItem(i, 3, QtWidgets.QTableWidgetItem(time.status))
            
    def refresh_diagnostics(self):
        if not self.g2:
            return
            
        try:
            diag = self.g2.get_diagnostics()
            self.diag_text.setPlainText(
                json.dumps(diag, indent=2))
        except Exception as e:
            self.diag_text.setPlainText(f"Error getting diagnostics: {str(e)}")
