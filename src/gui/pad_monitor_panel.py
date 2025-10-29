"""
Touch Pad Monitoring Panel
"""
from PySide6 import QtWidgets, QtCore, QtGui
from ..timing.g2_controller import G2Controller, G2PadStatus

class PadMonitorPanel(QtWidgets.QWidget):
    def __init__(self, g2: G2Controller, parent=None):
        super().__init__(parent)
        self.g2 = g2
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # Pad status grid
        self.pad_grid = QtWidgets.QGridLayout()
        self.pad_indicators = {}
        
        for lane in range(1, 9):
            label = QtWidgets.QLabel(f"Lane {lane}")
            status = QtWidgets.QLabel()
            status.setMinimumSize(100, 30)
            status.setAlignment(QtCore.Qt.AlignCenter)
            
            self.pad_indicators[lane] = status
            self.pad_grid.addWidget(label, lane-1, 0)
            self.pad_grid.addWidget(status, lane-1, 1)
        
        # Controls
        controls = QtWidgets.QHBoxLayout()
        
        self.calibrate_btn = QtWidgets.QPushButton("Calibrate All")
        self.calibrate_btn.clicked.connect(self.calibrate_pads)
        
        self.noise_btn = QtWidgets.QPushButton("Check Noise")
        self.noise_btn.clicked.connect(self.check_noise)
        
        controls.addWidget(self.calibrate_btn)
        controls.addWidget(self.noise_btn)
        
        # Add to main layout
        layout.addLayout(self.pad_grid)
        layout.addLayout(controls)
        
        # Update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(500)  # Update every 500ms
        
    def update_status(self):
        if not self.g2:
            return
            
        try:
            status = self.g2.get_pad_status()
            for lane, pad_status in status.items():
                indicator = self.pad_indicators.get(lane)
                if indicator:
                    self._update_indicator(indicator, pad_status)
        except Exception as e:
            print(f"Failed to update pad status: {e}")
            
    def _update_indicator(self, indicator: QtWidgets.QLabel, status: G2PadStatus):
        colors = {
            G2PadStatus.NORMAL: "#44cc44",    # Green
            G2PadStatus.BLOCKED: "#ff4444",    # Red
            G2PadStatus.DISABLED: "#666666",   # Gray
            G2PadStatus.NOISE: "#ffaa00"      # Orange
        }
        
        indicator.setStyleSheet(f"""
            QLabel {{
                background-color: {colors.get(status, "#ffffff")};
                border: 1px solid #000000;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }}
        """)
        indicator.setText(status.value)
        
    def calibrate_pads(self):
        if not self.g2:
            return
            
        try:
            results = self.g2.calibrate_pads()
            message = "Calibration results:\n"
            for lane, success in results.items():
                message += f"Lane {lane}: {'OK' if success else 'Failed'}\n"
                
            QtWidgets.QMessageBox.information(self, "Calibration", message)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Calibration failed: {e}")
            
    def check_noise(self):
        if not self.g2:
            return
            
        try:
            levels = self.g2.get_noise_levels()
            message = "Noise levels:\n"
            for lane, level in levels.items():
                message += f"Lane {lane}: {level:.2f}mV\n"
                
            QtWidgets.QMessageBox.information(self, "Noise Levels", message)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to get noise levels: {e}")
