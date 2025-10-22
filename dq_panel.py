from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class DQPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.dqs = []  # Each DQ: {"name": ..., "heat": ..., "reason": ..., "notes": ...}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Heat", "Reason", "Notes"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_dqs(self, dqs):
        self.dqs = dqs
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for dq in self.dqs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(dq["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(dq["heat"])))
            self.table.setItem(row, 2, QTableWidgetItem(dq["reason"]))
            self.table.setItem(row, 3, QTableWidgetItem(dq["notes"]))
