import sys
from PyQt5.QtWidgets import QApplication
from src.widgets.mainwidget import MainWindow
import src.parser.srt_parser as srt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    subtitles = srt.parse_srt('data/01 _ Brilliant Girls01.zh.srt')
    window = MainWindow(subtitles)
    window.show()
    sys.exit(app.exec_())
