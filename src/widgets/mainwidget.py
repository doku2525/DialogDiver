from PyQt5.QtWidgets import QVBoxLayout, QWidget

from src.widgets.srtviewerwidget import SRTViewer
from src.widgets.timelinewidget import Timeline


class MainWindow(QWidget):
    def __init__(self, subtitles):
        self.subtitles = subtitles
        super().__init__()
        self.viewer = SRTViewer(subtitles)
        self.timeline = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.viewer = SRTViewer(self.subtitles)
        self.timeline = Timeline(total_duration=2700, subtitles=self.subtitles)  # 45 Minuten in Sekunden
        layout.addWidget(self.viewer)
        layout.addWidget(self.timeline)
        self.setLayout(layout)
        self.setWindowTitle("DialogDiver - Zeitleiste")
        self.resize(800, 200)
