from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem,
                             QVBoxLayout, QWidget, QGraphicsRectItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainter, QBrush, QColor


class Timeline(QGraphicsView):
    def __init__(self, total_duration, subtitles=None, parent=None):
        super().__init__(parent)
        self.total_duration = total_duration  # Gesamtdauer in Sekunden
        self.zoom_level = 1.0
        self.max_y = self.width()
        self.subtitles = subtitles
        self.scene = None
        self.setFixedHeight(100)
        self.initUI()

    def initUI(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Zeichne die Zeitleiste
        self.draw_timeline()
        self.draw_subtitles()

    def mousePressEvent(self, event):
        # Überprüfen, ob es sich um einen Linksklick handelt
        if event.button() == Qt.MouseButton.LeftButton:
            # Umrechnen der View-Koordinaten in Szenen-Koordinaten
            scene_pos = self.mapToScene(event.pos())
            x_coordinate = scene_pos.x()
            # Hier hast du die x-Koordinate in self.scene
            print(f"Klick auf x-Koordinate: {x_coordinate}")
            # Optional: Weiterverarbeitung der Koordinate
            self.handle_click(x_coordinate)

        # Rufe die Standard-Event-Handler auf (wichtig für andere Funktionen)
        super().mousePressEvent(event)

    def handle_click(self, x):
        # Hier kannst du die Logik für die Behandlung des Klicks implementieren
        # z.B. die Zeit berechnen, die dem x-Wert entspricht
        time = self.x_to_time(x)
        print(f"Geklickte Zeit: {self.format_time(time)}")

    def x_to_time(self, x):
        # Umrechnen von x-Koordinaten in Zeit basierend auf der Gesamtbreite
        return (x / (self.width() * self.zoom_level)) * self.total_duration

    def draw_timeline(self):
        self.scene.clear()  # Wichtig: Szene vor dem Neuzeichnen leeren!
        scene_width = self.width() * self.zoom_level  # Breite der Szene berechnen
        self.scene.setSceneRect(0, 0, scene_width,
                                120)  # Größe der Szene anpassen. Hier wird auch der y-Wert und die Höhe angepasst.

        # Zeichne die Hauptlinie der Zeitleiste
        line = QGraphicsLineItem(0, 0, self.width(), 0)
        self.scene.addItem(line)

        # Füge Markierungen und Beschriftungen hinzu
        interval = 300  # 5 Minuten in Sekunden
        print(f"{self.zoom_level = } {interval * self.zoom_level = } {interval = } {self.max_y = } {self.width() = } {self.scene.width() = }")
        while interval * self.zoom_level > self.max_y and interval > 1:
            print(f"inside {interval * self.zoom_level = } {interval = }")
            interval = int(interval / (5 if interval > 60 else 6 if interval > 10 else 10))
            if interval < 1:
                interval = 1

        font = QFont("Arial", 8)
        print(f"{self.total_duration = } {interval =}")
        for time in range(0, self.total_duration + 1, interval):
            x = self.time_to_x(time)
            # Zeichne eine Markierung
            # marker = QGraphicsLineItem(x, 30, x, 34)
            marker = QGraphicsLineItem(x, 0, x, 55)
            self.scene.addItem(marker)
            # Füge eine Beschriftung hinzu
            label = QGraphicsTextItem(self.format_time(time)[:-4])
            label.setFont(font)
            # label.setPos(x - label.boundingRect().width() / 2, 35)
            label.setPos(x - label.boundingRect().width() / 2, 55)
            self.scene.addItem(label)

    def draw_subtitles(self):
        # Zeichne Boxen für jeden Untertitel
        for subtitle in self.subtitles:
            start_x = self.time_to_x(self.timecode_to_seconds(subtitle['start_time']))
            end_x = self.time_to_x(self.timecode_to_seconds(subtitle['end_time']))
            width = end_x - start_x
            height = 20  # Höhe der Box

            # Erstelle eine Box für den Untertitel
            box = QGraphicsRectItem(start_x, 30, width, height)
            box.setBrush(QBrush(QColor(100, 150, 255, 100)))  # Farbe der Box (blau mit Transparenz)
            self.scene.addItem(box)

            # Füge den Text des Untertitels hinzu
            # text = QGraphicsTextItem(subtitle['text'])
            # text.setPos(start_x + 5, 35)  # Positioniere den Text innerhalb der Box
            # text.setFont(QFont("Arial", 8))
            # self.scene.addItem(text)

    def timecode_to_seconds(self, timecode: str) -> float:
        """
        Konvertiert einen SRT-Zeitstempel (HH:MM:SS,MS) in Sekunden.
        """
        # print(f"{timecode = }")
        hours, minutes, seconds_milliseconds = timecode.split(':')
        seconds, milliseconds = seconds_milliseconds.split(',')
        return (
                int(hours) * 3600  # Stunden in Sekunden
                + int(minutes) * 60  # Minuten in Sekunden
                + int(seconds)  # Sekunden
                + int(milliseconds) / 1000  # Millisekunden in Sekunden
        )

    def time_to_x(self, time):
        # Konvertiere Zeit in x-Koordinaten basierend auf der Gesamtbreite
        # print( f"{ time = }")
        return (time / self.total_duration) * self.width() * self.zoom_level

    def format_time(self, time_in_s):
        # Konvertiere Sekunden in ein Zeitformat (MM:SS)
        minutes = int(time_in_s // 60)
        seconds = int(time_in_s % 60)
        millis = round(time_in_s - int(time_in_s),3) * 1000
        return f"{minutes:02}:{seconds:02}.{millis:03}"

    def wheelEvent(self, event):
        # Implementiere das Zoomen mit dem Mausrad
        zoom_factor = 1.25
        if event.angleDelta().y() > 0:
            self.zoom_level *= zoom_factor
        else:
            self.zoom_level /= zoom_factor
        if self.zoom_level < 1:
            self.zoom_level = 1
        #self.scale(zoom_factor if event.angleDelta().y() > 0 else 1 / zoom_factor, 1.0)
        self.update_legend()

    def update_legend(self):
        # Aktualisiere die Legende basierend auf dem Zoom-Level
        self.scene.clear()
        self.draw_timeline()
        self.draw_subtitles()
