from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem
from io.csv_importer import import_entries_from_csv, export_entries_to_csv

class EntriesPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import CSV")
        self.import_btn.clicked.connect(self.import_csv)
        self.export_btn = QPushButton("Export CSV")
        self.export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.export_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Heat", "Lane", "Status"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def import_csv(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Import Entries", "", "CSV Files (*.csv)")
        if not fname:
            return
        self.entries = import_entries_from_csv(fname)
        self.refresh_table()

    def export_csv(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Entries", "", "CSV Files (*.csv)")
        if not fname:
            return
        export_entries_to_csv(self.entries, fname)

    def refresh_table(self):
        self.table.setRowCount(0)
        for entry in self.entries:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, key in enumerate(["entry_id", "name", "heat", "lane", "status"]):
                self.table.setItem(row, i, QTableWidgetItem(str(getattr(entry, key))))
