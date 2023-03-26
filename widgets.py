""" Widgets for RobotGUI """

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLineEdit, QLabel, QWidget)
from PyQt5.QtCore import Qt


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

class ColorBlock(QFrame):
    """
    A simple widget ot show a single color
    """
    def __init__(self) -> None:
        super(ColorBlock, self).__init__()

        self.setFrameShape(QFrame.Box)
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
        color_str = rgb_to_hex((int(red),int(green), int(blue)))
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

class ConnStatus(QFrame):
    def __init__(self, text = "") -> None:
        super(ConnStatus, self).__init__()

        self.setFrameShape(QFrame.Shape.Box)
        self.setStyleSheet("background-color: #ef5350;")
        self.setMinimumHeight(48)


        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__text = QLabel(text)
        self.__text.setStyleSheet("font-weight: bold;")
        self.__text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__text)
