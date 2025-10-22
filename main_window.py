from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.timer_panel import TimerPanel
from gui.entries_panel import EntriesPanel
from gui.results_panel import ResultsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raceclock Time Machine G2 Controller")
        self.tabs = QTabWidget()
        self.timer_panel = TimerPanel()
        self.entries_panel = EntriesPanel()
        self.results_panel = ResultsPanel(results_panel=self.results_panel, 
entries_panel=self.entries_panel)
        self.tabs.addTab(self.timer_panel, "Timer")
        self.tabs.addTab(self.entries_panel, "Entries")
        self.tabs.addTab(self.results_panel, "Results")
        self.setCentralWidget(self.tabs)
        
