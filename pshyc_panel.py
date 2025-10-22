from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class PsychPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.psych_data = []  # Each: {"rank": ..., "name": ..., "seed": ..., "heat": ...}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Rank", "Name", "Seed", "Heat"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_psych(self, psych_data):
        self.psych_data = psych_data
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for item in self.psych_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item["rank"])))
            self.table.setItem(row, 1, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["seed"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["heat"])))
