"""
G2 Diagnostics Panel
"""
from PySide6 import QtWidgets, QtCore, QtGui
from ..timing.g2_controller import G2Controller
from ..timing.g2_error_handler import G2ErrorHandler, G2ErrorSeverity

class DiagnosticsPanel(QtWidgets.QWidget):
    def __init__(self, g2: G2Controller, error_handler: G2ErrorHandler, parent=None):
        super().__init__(parent)
        self.g2 = g2
        self.error_handler = error_handler
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # System status
        status_group = QtWidgets.QGroupBox("System Status")
        status_layout = QtWidgets.QGridLayout()
        
        self.conn_status = QtWidgets.QLabel()
        self.battery_status = QtWidgets.QLabel()
        self.memory_status = QtWidgets.QLabel()
        
        status_layout.addWidget(QtWidgets.QLabel("Connection:"), 0, 0)
        status_layout.addWidget(self.conn_status, 0, 1)
        status_layout.addWidget(QtWidgets.QLabel("Battery:"), 1, 0)
        status_layout.addWidget(self.battery_status, 1, 1)
        status_layout.addWidget(QtWidgets.QLabel("Memory:"), 2, 0)
        status_layout.addWidget(self.memory_status, 2, 1)
        
        status_group.setLayout(status_layout)
        
        # Error log
        error_group = QtWidgets.QGroupBox("Error Log")
        error_layout = QtWidgets.QVBoxLayout()
        
        self.error_table = QtWidgets.QTableWidget()
        self.error_table.setColumnCount(4)
        self.error_table.setHorizontalHeaderLabels(
            ["Time", "Severity", "Code", "Message"])
        
        error_controls = QtWidgets.QHBoxLayout()
        self.clear_btn = QtWidgets.QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_error_log)
        self.severity_combo = QtWidgets.QComboBox()
        self.severity_combo.addItems([s.value for s in G2ErrorSeverity])
        self.severity_combo.currentTextChanged.connect(self.filter_errors)
        
        error_controls.addWidget(QtWidgets.QLabel("Severity:"))
        error_controls.addWidget(self.severity_combo)
        error_controls.addWidget(self.clear_btn)
        
        error_layout.addWidget(self.error_table)
        error_layout.addLayout(error_controls)
        error_group.setLayout(error_layout)
        
        # Add to main layout
        layout.addWidget(status_group)
        layout.addWidget(error_group)
        
        # Update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)  # Update every second
        
    def update_status(self):
        if not self.g2:
            return
            
        try:
            # Update connection status
            self.conn_status.setText(self.g2.status.value)
            
            # Update battery status
            battery = self.g2.get_battery_status()
            self.battery_status.setText(
                f"Main: {battery['main']}V, Backup: {battery['backup']}V")
            
            # Update memory status
            diag = self.g2.get_diagnostics()
            self.memory_status.setText(
                f"Used: {diag.get('memory_used', 0)}%, Free: {diag.get('memory_free', 0)}%")
            
            # Update error log
            self.update_error_log()
            
        except Exception as e:
            print(f"Failed to update diagnostics: {e}")
            
    def update_error_log(self):
        severity = G2ErrorSeverity(self.severity_combo.currentText())
        errors = self.error_handler.get_recent_errors(severity=severity)
        
        self.error_table.setRowCount(len(errors))
        for i, error in enumerate(errors):
            self.error_table.setItem(i, 0, 
                QtWidgets.QTableWidgetItem(error.timestamp.strftime("%H:%M:%S")))
            self.error_table.setItem(i, 1,
                QtWidgets.QTableWidgetItem(error.severity.value))
            self.error_table.setItem(i, 2,
                QtWidgets.QTableWidgetItem(error.code.value))
            self.error_table.setItem(i, 3,
                QtWidgets.QTableWidgetItem(error.message))
            
    def clear_error_log(self):
        if self.error_handler:
            self.error_handler.clear_history()
            self.update_error_log()
            
    def filter_errors(self):
        self.update_error_log()
