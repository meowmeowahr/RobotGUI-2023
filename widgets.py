""" Widgets for RobotGUI """

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QLabel, QWidget

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
