""" The about box used in RobotGUI """

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QBasicTimer, QSize
from PyQt5.QtGui import QFont, QPalette, QPainter, QColor, QFontMetrics

import strings


class _WigglyWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(_WigglyWidget, self).__init__(parent)

        self.setBackgroundRole(QPalette.Midlight)
        self.setAutoFillBackground(True)

        new_font = self.font()
        new_font.setPointSize(new_font.pointSize() + 20)
        self.setFont(new_font)

        self.timer = QBasicTimer()
        self.text = ''

        self.step = 0
        self.timer.start(60, self)

    def paintEvent(self, _):
        sine_table = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)

        metrics = QFontMetrics(QFont(QFont.defaultFamily(QFont()), 22))
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QColor()

        painter = QPainter(self)

        for i, ch in enumerate(self.text):
            index = (self.step + i) % 16
            color.setHsv((15 - i) * 16, 255, 191)
            painter.setPen(color)
            painter.setFont(QFont(QFont.defaultFamily(QFont()), 22))
            painter.drawText(int(x), int(y) - int((sine_table[index] * metrics.height()) / 600), ch)
            x += metrics.width(ch)

    def setText(self, new_text: str) -> None:
        self.text = new_text

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            self.update()
        else:
            super(_WigglyWidget, self).timerEvent(event)


class AboutBox(QWidget):
    def __init__(self):
        super(AboutBox, self).__init__()

        self.setWindowTitle(strings.WINDOW_TITLE)

        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)

        self.__ee_cnt = 0

        self.title = QLabel(strings.WINDOW_TITLE)
        self.title.setStyleSheet("font-size: 26px;")
        self.title.mouseReleaseEvent = self.__ee_event
        self.title.setAlignment(Qt.AlignCenter)
        self.root_layout.addWidget(self.title)

        self.version = QLabel()
        self.version.setAlignment(Qt.AlignCenter)
        self.root_layout.addWidget(self.version)

        self.__ee = _WigglyWidget()
        self.__ee.setText(strings.ROBOT_NAME_EE)
        self.__ee.setFixedSize(QSize(256, 96))
        self.__ee.hide()
        self.root_layout.addWidget(self.__ee, alignment=Qt.AlignCenter)

    def __ee_event(self, _):
        self.__ee_cnt += 1
        if self.__ee_cnt >= 15:
            self.__ee.show()
