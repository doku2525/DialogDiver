import sys
from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget


class SRTViewer(QWidget):

    def __init__(self, subtitles):
        super().__init__()
        self.subtitles = subtitles
        self.initUI()
        self.listWidget = None
        self.setMinimumHeight(600)

    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()
        for subtitle in self.subtitles:
            self.listWidget.addItem(f"{subtitle['start_time']} - {subtitle['end_time']}: {subtitle['text']}")
        layout.addWidget(self.listWidget)
        self.setLayout(layout)
        self.setWindowTitle('SRT Viewer')
        self.show()
