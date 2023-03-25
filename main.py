"""
RobotGUI
"""

import logging
import argparse
import json
import sys
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QLabel,
                             QTabWidget, QWidget, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QCheckBox,
                             QProgressBar)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize

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
parser.add_argument("-s", "--settings", help="location of settings file",
                    required=False,
                    default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                         "settings.json"))
args = parser.parse_args()

red = 0
green = 0
blue = 0


def value_changed(_, key, value, is_new):
    """ Callback for Network Tables """
    logging.debug(f"valueChanged: key: '{key}'; value: {value}; isNew: {is_new}")

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
            get_updater().call_latest(window.s_p.setText,
                                      stringcase.titlecase(str(value).replace('Neither', 'None')))
        elif key == 'PickPos':
            get_updater().call_latest(window.s_p.setText,
                                      stringcase.titlecase(str(value).replace('Neither', 'None')))

def color_value_changed(_, key, value, is_new):
    """ Callback for Network Tables """
    global red, green, blue
    logging.debug(f"colorValueChanged: key: '{key}'; value: {value}; isNew: {is_new}")

    if "window" in globals().keys():
        if key == "colorSensorRed":
            red = float(value)
            get_updater().call_latest(window.color_red.setText, f"Red: {red}")
            get_updater().call_latest(window.color_red_bar.setValue, int(red))
        elif key == "colorSensorGreen":
            green = float(value)
            get_updater().call_latest(window.color_green.setText, f"Green: {green}")
            get_updater().call_latest(window.color_green_bar.setValue, int(green))
        elif key == "colorSensorBlue":
            blue = float(value)
            get_updater().call_latest(window.color_blue.setText, f"Blue: {blue}")
            get_updater().call_latest(window.color_blue_bar.setValue, int(blue))

        get_updater().call_latest(window.color.setRGB, red, green, blue)

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

        self.setup = Settings()

        self.file_menu = self.menu.addMenu(strings.MENU_FILE)
        self.file_menu.addAction(strings.MENU_SETUP, self.setup.show)
        self.file_menu.addAction(strings.MENU_QUIT, self.close)

        self.help_menu = self.menu.addMenu(strings.MENU_HELP)
        self.help_menu.addAction(strings.MENU_ABOUT, self.about.show)
        self.help_menu.addAction(strings.MENU_ABOUT_QT, QApplication.instance().aboutQt)

        self.setMenuBar(self.menu)

        # Layout
        self.root_widget = QTabWidget(self)
        self.setCentralWidget(self.root_widget)

        self.object_tab_widget = QWidget()
        self.object_tab_layout = QGridLayout()
        self.object_tab_widget.setLayout(self.object_tab_layout)
        self.root_widget.addTab(self.object_tab_widget, strings.TAB_OBJECT)

        self.color_tab_widget = QWidget()
        self.color_tab_layout = QHBoxLayout()
        self.color_tab_widget.setLayout(self.color_tab_layout)
        self.root_widget.addTab(self.color_tab_widget, strings.TAB_COLOR)

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

        # Color
        self.color = widgets.ColorBlock()
        self.color.setFixedSize(QSize(240, 240))
        self.color_tab_layout.addWidget(self.color)

        self.color_side_layout = QVBoxLayout()
        self.color_tab_layout.addLayout(self.color_side_layout)

        self.color_red = QLabel("Red: Unknown")
        self.color_side_layout.addWidget(self.color_red)

        self.color_red_bar = QProgressBar()
        self.color_red_bar.setRange(0, 255)
        self.color_red_bar.setStyleSheet("QProgressBar::chunk { background-color: #f44336; }")
        self.color_side_layout.addWidget(self.color_red_bar)

        self.color_green = QLabel("Green: Unknown")
        self.color_side_layout.addWidget(self.color_green)

        self.color_green_bar = QProgressBar()
        self.color_green_bar.setRange(0, 255)
        self.color_green_bar.setStyleSheet("QProgressBar::chunk { background-color: #4caf50; }")
        self.color_side_layout.addWidget(self.color_green_bar)

        self.color_blue = QLabel("Blue: Unknown")
        self.color_side_layout.addWidget(self.color_blue)

        self.color_blue_bar = QProgressBar()
        self.color_blue_bar.setRange(0, 255)
        self.color_blue_bar.setStyleSheet("QProgressBar::chunk { background-color: #2196f3; }")
        self.color_side_layout.addWidget(self.color_blue_bar)

        self.show()


class Settings(QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()

        self.setWindowTitle(strings.SETUP_WINDOW_TITLE)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Theme
        self.theme_widget = QWidget()
        self.theme_layout = QVBoxLayout()
        self.theme_widget.setLayout(self.theme_layout)
        self.tabs.addTab(self.theme_widget, strings.TAB_SETUP_THEME)

        self.theme_dark_mode = QCheckBox(strings.CHECK_DARK_MODE)
        self.theme_dark_mode.setChecked(settings["dark_mode"])
        self.theme_dark_mode.clicked.connect(lambda: self.enable_setting("dark_mode", self.theme_dark_mode.isChecked()))
        self.theme_layout.addWidget(self.theme_dark_mode)

        # Connection
        self.conns_widget = QWidget()
        self.conns_layout = QVBoxLayout()
        self.conns_widget.setLayout(self.conns_layout)
        self.tabs.addTab(self.conns_widget, strings.TAB_SETUP_CONNS)

        self.conns_warning = QLabel(strings.LABEL_CONNS_WARNING)
        self.conns_layout.addWidget(self.conns_warning)

        self.ip_editor = widgets.QNamedLineEdit(strings.EDIT_SETUP_IP)
        self.ip_editor.lineedit.setPlaceholderText(strings.EDIT_SETUP_IP_PLHOLD)
        self.ip_editor.lineedit.setText(settings["ip"])
        self.ip_editor.lineedit.textChanged.connect(lambda: self.update_setting("ip", self.ip_editor.lineedit.text()))
        self.conns_layout.addWidget(self.ip_editor)

    def enable_setting(self, key, enabled=True):
        settings[key] = enabled

        if key == "dark_mode":
            if settings["dark_mode"]:
                qt_material.apply_stylesheet(app, theme="dark_red.xml")
            else:
                qt_material.apply_stylesheet(app, theme="light_red.xml")

        with open(args.settings, "w", encoding="UTF-8") as file:
            json.dump(settings, file, indent=2)

    def update_setting(self, key, value):
        settings[key] = value

        with open(args.settings, "w", encoding="UTF-8") as file:
            json.dump(settings, file, indent=2)

if __name__ == "__main__":
    with open(args.settings, encoding="UTF-8") as file:
        settings = json.load(file)

    logging.basicConfig(level=settings["log_level"])

    logging.debug(f"Loaded settings from {args.settings}")

    app = QApplication(sys.argv)
    if settings["dark_mode"]:
        qt_material.apply_stylesheet(app, theme="dark_red.xml")
    else:
        qt_material.apply_stylesheet(app, theme="light_red.xml")
    window = MainWindow()

    NetworkTables.initialize(server=settings["ip"])
    sd = NetworkTables.getTable("SmartDashboard")
    color = NetworkTables.getTable("RevColorSensor_V3")
    sd.addEntryListener(value_changed)  # has to be done after setting up window
    color.addEntryListener(color_value_changed)  # has to be done after setting up window

    sys.exit(app.exec())
