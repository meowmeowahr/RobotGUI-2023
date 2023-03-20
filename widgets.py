""" Widgets for RobotGUI """

from PyQt5.QtWidgets import QFrame

class ColorBlock(QFrame):
    """
    A simple widget ot show a single color
    """
    def __init__(self):
        super(ColorBlock, self).__init__()

        self.setFrameShape(QFrame.Box)
        self.setMinimumWidth(64)

        self.setMaximumSize(128, 128)

    def setColor(self, color: str) -> None:
        """
        Sets the color of the widget
        """
        self.setStyleSheet(f"background-color: {color};")
