"""
RobotGUI
"""

import logging
import argparse
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow,
                            QMenuBar, QLabel, QTabWidget, QWidget, QGridLayout)
from PyQt5.QtGui import QFont

from qt_thread_updater import get_updater
import qt_material

from networktables import NetworkTables
import stringcase

import about
import strings
import widgets


__version__ = "0.1.0"

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip", help="ip address to connect to",
                    required=False, default="10.63.69.2")
args = parser.parse_args()


def value_changed(_, key, value, is_new):
    """ Callback for Network Tables """
    print(f"valueChanged: key: '{key}'; value: {value}; isNew: {is_new}")

    if "window" in globals().keys():
        if key == 'Mode':
            get_updater().call_latest(window.arm_mode.setText, str(value).replace("_", " ").title())
            if str(value) == "Scoring":
                get_updater().call_latest(window.arm_mode_color.setColor, "#4caf50")
            elif str(value) == "Picking_up":      
                get_updater().call_latest(window.arm_mode_color.setColor, "#00bcd4")
            else:
                get_updater().call_latest(window.arm_mode_color.setColor, "#fafafa")
        elif key == 'Object':
            get_updater().call_latest(window.arm_obj.setText, str(value).replace('Neither', 'None')
                                      .replace("_", " ").title())
            if str(value) == "Cube":
                get_updater().call_latest(window.arm_obj_mode_color.setColor, "#9c27b0")
            elif str(value) == "Cone":
                get_updater().call_latest(window.arm_obj_mode_color.setColor, "#fdd835")
            else:
                get_updater().call_latest(window.arm_obj_mode_color.setColor, "#fafafa")
        elif key == 'ScorePos':
            get_updater().call_latest(window.s_p.setText, stringcase.titlecase(str(value).replace('Neither', 'None')))
        elif key == 'PickPos':
            get_updater().call_latest(window.s_p.setText, stringcase.titlecase(str(value).replace('Neither', 'None')))


class MainWindow(QMainWindow):
    """ Main Window for RobotGUI """

    # noinspection PyTypeChecker
    def __init__(self):
        super(MainWindow, self).__init__()

        # Title
        self.setWindowTitle(strings.WINDOW_TITLE)

        # Menu
        self.menu = QMenuBar(self)

        self.about = about.AboutBox()
        self.about.version.setText(__version__)

        self.file_menu = self.menu.addMenu(strings.MENU_FILE)
        self.file_menu.addAction(strings.MENU_ABOUT, self.about.show)
        self.file_menu.addAction(strings.MENU_QUIT, self.close)

        self.setMenuBar(self.menu)

        # Layout
        self.root_widget = QTabWidget(self)
        self.setCentralWidget(self.root_widget)

        self.object_tab_widget = QWidget()
        self.object_tab_layout = QGridLayout()
        self.object_tab_widget.setLayout(self.object_tab_layout)
        self.root_widget.addTab(self.object_tab_widget, strings.TAB_OBJECT)

        # Arm Mode
        self.arm_mode_label = QLabel("Arm Mode:")
        self.arm_mode_label.setStyleSheet("font-size: 50px;")
        self.object_tab_layout.addWidget(self.arm_mode_label, 0, 0)

        self.arm_mode = QLabel("Unknown")
        self.arm_mode.setStyleSheet("font-size: 64px;")
        self.object_tab_layout.addWidget(self.arm_mode, 0, 1)

        self.arm_mode_color = widgets.ColorBlock()
        self.arm_mode_color.setColor("#fafafa")
        self.object_tab_layout.addWidget(self.arm_mode_color, 0, 2)

        # Arm Object
        self.arm_obj_label = QLabel("Arm Object:")
        self.arm_obj_label.setStyleSheet("font-size: 50px;")
        self.object_tab_layout.addWidget(self.arm_obj_label, 1, 0)

        self.arm_obj = QLabel("Unknown")
        self.arm_obj.setStyleSheet("font-size: 64px;")
        self.arm_obj.setFont(QFont(QFont.defaultFamily(QFont()), 22))
        self.object_tab_layout.addWidget(self.arm_obj, 1, 1)

        self.arm_obj_mode_color = widgets.ColorBlock()
        self.arm_obj_mode_color.setColor("#fafafa")
        self.object_tab_layout.addWidget(self.arm_obj_mode_color, 1, 2)

        # Position
        self.sp_label = QLabel("S/PU Pos:")
        self.sp_label.setStyleSheet("font-size: 50px;")
        self.object_tab_layout.addWidget(self.sp_label, 2, 0)

        self.s_p = QLabel("Unknown")
        self.s_p.setStyleSheet("font-size: 64px;")
        self.s_p.setFont(QFont(QFont.defaultFamily(QFont()), 22))
        self.object_tab_layout.addWidget(self.s_p, 2, 1)

        self.sp_color = widgets.ColorBlock()
        self.sp_color.setColor("#fafafa")
        self.object_tab_layout.addWidget(self.sp_color, 2, 2)

        self.show()


if __name__ == "__main__":
    # NetTables
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)
    qt_material.apply_stylesheet(app, theme="dark_red.xml")
    window = MainWindow()

    NetworkTables.initialize(server=args.ip)
    sd = NetworkTables.getTable("SmartDashboard")
    sd.addEntryListener(value_changed)  # has to be done after setting up window

    sys.exit(app.exec())
