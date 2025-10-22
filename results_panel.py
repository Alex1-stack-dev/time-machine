from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem
from io.csv_exporter import export_results_to_csv
from io.pdf_exporter import export_results_to_pdf

class ResultsPanel(QWidget):
    def __init__(self, results_panel=None, entries_panel=None):
        super().__init__()
        self.results = []  # Populate from timer splits or external source
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.export_csv_btn = QPushButton("Export CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_pdf_btn = QPushButton("Export PDF")
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        btn_layout.addWidget(self.export_csv_btn)
        btn_layout.addWidget(self.export_pdf_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Place", "Name", "Time", "Heat", "DQ"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_results(self, results):
        self.results = results
        self.refresh_table()

    def export_csv(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if not fname:
            return
        export_results_to_csv(self.results, fname)

    def export_pdf(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "PDF Files (*.pdf)")
        if not fname:
            return
        export_results_to_pdf(self.results, fname)

    def refresh_table(self):
        self.table.setRowCount(0)
        for result in self.results:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, key in enumerate(["place", "name", "time", "heat", "dq"]):
                self.table.setItem(row, i, QTableWidgetItem(str(getattr(result, key))))
