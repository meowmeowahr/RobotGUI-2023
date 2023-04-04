""" Widgets for RobotGUI """

from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QLabel, QWidget, QSpinBox, QPushButton)
from PyQt6.QtCore import Qt

import enum

import strings


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

class Serverity(enum.Enum):
    SEVERE = 0
    WARN = 1


class ColorBlock(QFrame):
    """
    A simple widget ot show a single color
    """
    def __init__(self) -> None:
        super(ColorBlock, self).__init__()

        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumWidth(64)

        self.setMaximumSize(128, 128)

    def setColor(self, color: str) -> None:
        """
        Sets the color of the widget
        """
        self.setStyleSheet(f"background-color: {color};")

    def setRGB(self, red, green, blue):
        """
        Sets the color of the widget in (r, g, b)
        """
        color_str = rgb_to_hex((int(red), int(green), int(blue)))
        self.setStyleSheet(f"background-color: #{color_str};")


class QNamedLineEdit(QWidget):
    """
    A Named QLineEdit
    """
    def __init__(self, text: str = ""):
        super().__init__()

        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.label = QLabel(text)
        self.__layout.addWidget(self.label)

        self.lineedit = QLineEdit()
        self.__layout.addWidget(self.lineedit)


class QNamedSpinBox(QWidget):
    """
    A Named QSpinBox
    """
    def __init__(self, text: str = ""):
        super().__init__()

        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.label = QLabel(text)
        self.__layout.addWidget(self.label)

        self.spin = QSpinBox()
        self.__layout.addWidget(self.spin)


class StatusBar(QFrame):
    def __init__(self, text="", closeable=False, severity=Serverity.SEVERE) -> None:
        super(StatusBar, self).__init__()

        self.closeable = closeable

        self.setFrameShape(QFrame.Shape.Box)
        if severity == Serverity.SEVERE:
            self.setStyleSheet("background-color: #ef5350;")
        elif severity == Serverity.WARN:
            self.setStyleSheet("background-color: #ffc107;")
        self.setMinimumHeight(48)

        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__text = QLabel(text)
        self.__text.setStyleSheet("font-weight: bold;")
        self.__text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__text)

    def mousePressEvent(self, QMouseEvent):
        if self.closeable:
            self.setVisible(False)


class Swerve(QWidget):
    def __init__(self, title: str = "Swerve") -> None:
        super(Swerve, self).__init__()

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        self.__frame = QFrame()
        self.__frame.setProperty('class', 'swerve_frame')
        self.__frame.setFrameShape(QFrame.Shape.Box)
        self.__layout.addWidget(self.__frame)

        self.__frame_layout = QVBoxLayout()
        self.__frame.setLayout(self.__frame_layout)

        self.title = QLabel(title)
        self.title.setProperty('class', 'swerve_title')
        self.__frame_layout.addWidget(self.title)

        self.__frame_layout.addStretch()

        self.cancoder_label = QLabel(strings.LABEL_CANCODER_TITLE)
        self.cancoder_label.setProperty('class', 'cancoder_title')
        self.__frame_layout.addWidget(self.cancoder_label)

        self.cancoder_value = QLabel(strings.UNKNOWN)
        self.__frame_layout.addWidget(self.cancoder_value)

        self.__frame_layout.addStretch()

        self.line = HLine()
        self.__frame_layout.addWidget(self.line)

        self.__frame_layout.addStretch()

        self.integrated_label = QLabel(strings.LABEL_INTEGRATED_TITLE)
        self.integrated_label.setProperty('class', 'integrated_title')
        self.__frame_layout.addWidget(self.integrated_label)

        self.integrated_value = QLabel(strings.UNKNOWN)
        self.__frame_layout.addWidget(self.integrated_value)

        self.__frame_layout.addStretch()

        self.line = HLine()
        self.__frame_layout.addWidget(self.line)

        self.__frame_layout.addStretch()

        self.velocity_label = QLabel(strings.LABEL_VELOCITY_TITLE)
        self.velocity_label.setProperty('class', 'velocity_title')
        self.__frame_layout.addWidget(self.velocity_label)

        self.velocity_value = QLabel(strings.UNKNOWN)
        self.__frame_layout.addWidget(self.velocity_value)

    def setCancoderValue(self, value: float) -> None:
        self.cancoder_value.setText(str(value))

    def setIntegratedValue(self, value: float) -> None:
        self.integrated_value.setText(str(value))

    def setVelocityValue(self, value: float) -> None:
        self.velocity_value.setText(str(value))


class HLine(QFrame):
    def __init__(self) -> None:
        super(HLine, self).__init__()

        self.setFrameStyle(QFrame.Shape.HLine)
