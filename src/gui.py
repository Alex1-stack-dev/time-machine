from PySide6 import QtCore, QtGui, QtWidgets
from pathlib import Path

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, version="0.0.0", check_update_callback=None):
        super().__init__()
        self.version = version
        self.check_update_callback = check_update_callback

        self.setWindowTitle(f"Time Machine — {self.version}")
        self.resize(1000, 700)
        self._build_ui()

    def _build_ui(self):
        # Central widget layout
        central = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout(central)

        # Left sidebar (meets / events)
        self.left_list = QtWidgets.QListWidget()
        self.left_list.addItems(["Championship Meet 2025", "Local Meet — May", "Practice Meet"])
        self.left_list.setMaximumWidth(280)
        hbox.addWidget(self.left_list)

        # Main content (grid-like)
        self.main_table = QtWidgets.QTableWidget(20, 6)
        self.main_table.setHorizontalHeaderLabels(["Lane", "Name", "Age", "Team", "Seed", "Time"])
        hbox.addWidget(self.main_table, 1)

        # Right pane (details)
        right_v = QtWidgets.QVBoxLayout()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        right_v.addWidget(self.details)

        # Buttons
        btn_check_update = QtWidgets.QPushButton("Check for updates")
        btn_check_update.clicked.connect(self.on_check_updates)
        right_v.addWidget(btn_check_update)

        hbox.addLayout(right_v)

        # Menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        exit_action = QtGui.QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        filemenu.addAction(exit_action)

        help_menu = menubar.addMenu("&Help")
        about_action = QtGui.QAction("&About")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.setCentralWidget(central)

    def show_about(self):
        QtWidgets.QMessageBox.information(self, "About", f"Time Machine\nVersion {self.version}\nInspired by Hy-Tek")

    def on_check_updates(self):
        if self.check_update_callback:
            self.check_update_callback(self)
