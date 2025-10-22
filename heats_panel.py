from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class HeatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.heats = []  # List of heats, each heat is a dict or object
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Heat #", "Lane", "Name"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_heats(self, heats):
        self.heats = heats
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for heat in self.heats:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(heat["heat_num"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(heat["lane"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(heat["name"])))
