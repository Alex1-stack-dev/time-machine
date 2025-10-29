import sys
from PySide6 import QtWidgets, QtCore
from pathlib import Path

VERSION = "0.1.0"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Time Machine v{VERSION}")
        self.resize(800, 600)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
