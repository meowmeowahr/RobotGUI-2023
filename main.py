"""
RobotGUI
"""

# System
import logging
import argparse
import json
import platform
import sys
import os
import re

from typing import Final

# Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QLabel,
                             QTabWidget, QWidget, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QCheckBox,
                             QProgressBar, QToolBar, QToolButton,
                             QPushButton)
from PyQt6.QtGui import QFont, QIcon, QCloseEvent, QGuiApplication
from PyQt6.QtCore import QSize, QTimer, QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Misc GUI
from qt_thread_updater import get_updater
import qt_material
import qtawesome

# Windows 10/11
if platform.system() == "Windows":
    from ctypes import byref, c_bool, sizeof, windll
    from ctypes.wintypes import BOOL

# Misc
from networktables import NetworkTables
import stringcase

import about
import strings
import widgets

import update_checker


__version__: Final[str] = "0.6.0"

DEFAULT_SETTINGS: Final[dict] = {
    "log_level": 20,
    "dark_mode": True,
    "ip": "10.63.69.2",
    "camera_http": "http://10.63.69.14:1181/stream.mjpg?1680129953477",
    "camera_screen": 1,
    "cam_fullscreen": True,
    "first_run": True,
    "repo": "meowmeowahr/RobotGUI-2023",
    "show_updates": True
}

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
prox = 0


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
        elif re.match(r"Mod \d Cancoder", key):
            module = int(str(key)[4])
            if module == 0:
                get_updater().call_latest(window.swerve_mod_0.setCancoderValue, value)
            elif module == 1:
                get_updater().call_latest(window.swerve_mod_1.setCancoderValue, value)
            elif module == 2:
                get_updater().call_latest(window.swerve_mod_2.setCancoderValue, value)
            elif module == 3:
                get_updater().call_latest(window.swerve_mod_3.setCancoderValue, value)
        elif re.match(r"Mod \d Integrated", key):
            module = int(str(key)[4])
            if module == 0:
                get_updater().call_latest(window.swerve_mod_0.setIntegratedValue, value)
            elif module == 1:
                get_updater().call_latest(window.swerve_mod_1.setIntegratedValue, value)
            elif module == 2:
                get_updater().call_latest(window.swerve_mod_2.setIntegratedValue, value)
            elif module == 3:
                get_updater().call_latest(window.swerve_mod_3.setIntegratedValue, value)
        elif re.match(r"Mod \d Velocity", key):
            module = int(str(key)[4])
            if module == 0:
                get_updater().call_latest(window.swerve_mod_0.setVelocityValue, value)
            elif module == 1:
                get_updater().call_latest(window.swerve_mod_1.setVelocityValue, value)
            elif module == 2:
                get_updater().call_latest(window.swerve_mod_2.setVelocityValue, value)
            elif module == 3:
                get_updater().call_latest(window.swerve_mod_3.setVelocityValue, value)


def color_value_changed(_, key, value, is_new):
    """ Callback for Network Tables """
    global red, green, blue, prox
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
        elif key == "colorSensorProx":
            prox = float(value)
            get_updater().call_latest(window.color_prox.setText, f"Prox: {prox}")
            get_updater().call_latest(window.color_prox_bar.setValue, int(prox))

        get_updater().call_latest(window.color.setRGB, red, green, blue)


def enable_setting(key, enabled=True):
    settings[key] = enabled

    if key == "dark_mode":
        if settings["dark_mode"]:
            qt_material.apply_stylesheet(app, theme="dark_red.xml", css_file="material-fixes.qss")
        else:
            qt_material.apply_stylesheet(app, theme="light_red.xml", css_file="material-fixes.qss")

        if platform.system() == "Windows":
            window.setup.set_windows_dark(settings["dark_mode"])
            window.set_windows_dark(settings["dark_mode"])
            cam.set_windows_dark(settings["dark_mode"])

    save_settings()


def save_settings():
    with open(args.settings, "w", encoding="UTF-8") as file:
        json.dump(settings, file, indent=2)


def update_setting(key, value):
    settings[key] = value

    save_settings()


def close_all_windows():
    window.setup.close()
    window.about.close()
    window.close()
    cam.close()


class MainWindow(QMainWindow):
    """ Main Window for RobotGUI """

    # noinspection PyTypeChecker
    def __init__(self):
        super(MainWindow, self).__init__()

        # Title
        self.setWindowTitle(strings.APP_NAME)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/icons/icon.svg")))

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
        self.root_widget = QWidget()
        self.setCentralWidget(self.root_widget)
        self.root_layout = QVBoxLayout()
        self.root_widget.setLayout(self.root_layout)

        # Connection
        self.connection_status_widget = widgets.StatusBar(strings.CONN_NOT_CONNECTED.format(settings["ip"]))
        self.root_layout.addWidget(self.connection_status_widget)

        self.connection_timer = QTimer()
        self.connection_timer.setInterval(1000)
        self.connection_timer.timeout.connect(self.update_conns)
        self.connection_timer.start()

        # Update
        if settings["show_updates"]:
            self.versions = update_checker.UpdateChecker(settings["repo"], __version__.strip("v"))  # GitHub releases

            self.update_status_widget = widgets.StatusBar(strings.UPDATE_AVAIL.format(self.versions.latest,
                                                                                      self.versions.current),
                                                          closeable=True, severity=widgets.Serverity.WARN)
            self.update_status_widget.setVisible(self.versions.newer_available)
            self.root_layout.addWidget(self.update_status_widget)

        # Tabs
        self.tab_widget = QTabWidget(self)
        self.root_layout.addWidget(self.tab_widget)

        self.object_tab_widget = QWidget()
        self.object_tab_layout = QGridLayout()
        self.object_tab_widget.setLayout(self.object_tab_layout)
        self.tab_widget.addTab(self.object_tab_widget, strings.TAB_OBJECT)

        self.color_tab_widget = QWidget()
        self.color_tab_layout = QHBoxLayout()
        self.color_tab_widget.setLayout(self.color_tab_layout)
        self.tab_widget.addTab(self.color_tab_widget, strings.TAB_COLOR)

        self.swerve_tab_widget = QWidget()
        self.swerve_tab_layout = QGridLayout()
        self.swerve_tab_widget.setLayout(self.swerve_tab_layout)
        self.tab_widget.addTab(self.swerve_tab_widget, strings.TAB_SWERVE)

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

        self.color_prox = QLabel("Prox: Unknown")
        self.color_side_layout.addWidget(self.color_prox)

        self.color_prox_bar = QProgressBar()
        self.color_prox_bar.setRange(0, 65535)
        self.color_side_layout.addWidget(self.color_prox_bar)

        # Swerve
        self.swerve_mod_0 = widgets.Swerve(strings.SWERVE_MOD.format(0))
        self.swerve_tab_layout.addWidget(self.swerve_mod_0, 0, 0)

        self.swerve_mod_1 = widgets.Swerve(strings.SWERVE_MOD.format(1))
        self.swerve_tab_layout.addWidget(self.swerve_mod_1, 0, 1)

        self.swerve_mod_2 = widgets.Swerve(strings.SWERVE_MOD.format(2))
        self.swerve_tab_layout.addWidget(self.swerve_mod_2, 1, 0)

        self.swerve_mod_3 = widgets.Swerve(strings.SWERVE_MOD.format(3))
        self.swerve_tab_layout.addWidget(self.swerve_mod_3, 1, 1)

        if platform.system() == "Windows":
            self.set_windows_dark(settings["dark_mode"])

        self.show()

    def set_windows_dark(self, dark: bool):
        if platform.system() == "Windows":
            windll.LoadLibrary("dwmapi").DwmSetWindowAttribute(int(self.winId()), 20, byref(c_bool(dark)), sizeof(BOOL))

    def update_conns(self):
        self.connection_status_widget.setVisible(not NetworkTables.isConnected())

    def closeEvent(self, a0: QCloseEvent) -> None:
        close_all_windows()
        a0.accept()


class Settings(QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()

        self.setWindowTitle(strings.SETUP_WINDOW_TITLE)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/icons/icon.svg")))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Theme
        self.theme_widget = QWidget()
        self.theme_layout = QVBoxLayout()
        self.theme_widget.setLayout(self.theme_layout)
        self.tabs.addTab(self.theme_widget, strings.TAB_SETUP_THEME)

        self.theme_dark_mode = QCheckBox(strings.CHECK_DARK_MODE)
        self.theme_dark_mode.setChecked(settings["dark_mode"])
        self.theme_dark_mode.clicked.connect(lambda: enable_setting("dark_mode", self.theme_dark_mode.isChecked()))
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
        self.ip_editor.lineedit.textChanged.connect(lambda: update_setting("ip", self.ip_editor.lineedit.text()))
        self.conns_layout.addWidget(self.ip_editor)

        self.cam_editor = widgets.QNamedLineEdit(strings.EDIT_SETUP_CAM)
        self.cam_editor.lineedit.setPlaceholderText(strings.EDIT_SETUP_CAM_PLHOLD)
        self.cam_editor.lineedit.setText(settings["camera_http"])
        self.cam_editor.lineedit.textChanged.connect(lambda: update_setting("camera_http",
                                                                            self.cam_editor.lineedit.text()))
        self.conns_layout.addWidget(self.cam_editor)

        # Cam
        self.cam_widget = QWidget()
        self.cam_layout = QVBoxLayout()
        self.cam_widget.setLayout(self.cam_layout)
        self.tabs.addTab(self.cam_widget, strings.TAB_SETUP_CAM)

        self.cam_warning = QLabel(strings.LABEL_CAM_WARNING)
        self.cam_layout.addWidget(self.cam_warning)

        self.cam_screen = widgets.QNamedSpinBox(strings.SPIN_CAM_SCREEN)
        self.cam_screen.spin.setRange(0, 5)
        self.cam_screen.spin.valueChanged.connect(lambda: update_setting("camera_screen", self.cam_screen.spin.value()))
        self.cam_layout.addWidget(self.cam_screen)

        if platform.system() == "Windows":
            self.set_windows_dark(settings["dark_mode"])

    def set_windows_dark(self, dark: bool):
        if platform.system() == "Windows":
            windll.LoadLibrary("dwmapi").DwmSetWindowAttribute(int(self.winId()), 20, byref(c_bool(dark)), sizeof(BOOL))


class CamMonitor(QMainWindow):
    def __init__(self):
        super(CamMonitor, self).__init__()

        self.setWindowTitle(strings.CAM_TITLE)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/icons/icon.svg")))

        self.web = QWebEngineView()
        self.web.setUrl(QUrl(settings["camera_http"]))

        self.toolbar = QToolBar(strings.CAM_TOOLBAR)
        self.addToolBar(self.toolbar)

        self.refresh_button = QToolButton()
        self.refresh_button.setIconSize(QSize(72, 72))
        self.refresh_button.setIcon(qtawesome.icon("mdi.refresh", color=os.environ["QTMATERIAL_PRIMARYCOLOR"]))
        self.refresh_button.clicked.connect(self.web.reload)
        self.toolbar.addWidget(self.refresh_button)

        self.zoom_in_button = QToolButton()
        self.zoom_in_button.setIconSize(QSize(72, 72))
        self.zoom_in_button.setIcon(qtawesome.icon("mdi.magnify-plus", color=os.environ["QTMATERIAL_PRIMARYCOLOR"]))
        self.zoom_in_button.clicked.connect(lambda: self.web.setZoomFactor(self.web.zoomFactor() + 0.2))
        self.toolbar.addWidget(self.zoom_in_button)

        self.zoom_out_button = QToolButton()
        self.zoom_out_button.setIconSize(QSize(72, 72))
        self.zoom_out_button.setIcon(qtawesome.icon("mdi.magnify-minus", color=os.environ["QTMATERIAL_PRIMARYCOLOR"]))
        self.zoom_out_button.clicked.connect(lambda: self.web.setZoomFactor(self.web.zoomFactor() - 0.2))
        self.toolbar.addWidget(self.zoom_out_button)

        self.fullscreen_button = QToolButton()
        self.fullscreen_button.setIconSize(QSize(72, 72))
        self.fullscreen_button.setIcon(qtawesome.icon("mdi.fullscreen", color=os.environ["QTMATERIAL_PRIMARYCOLOR"]))
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.toolbar.addWidget(self.fullscreen_button)

        self.exit_button = QToolButton()
        self.exit_button.setIconSize(QSize(72, 72))
        self.exit_button.setIcon(qtawesome.icon("mdi.close", color=os.environ["QTMATERIAL_PRIMARYCOLOR"]))
        self.exit_button.clicked.connect(close_all_windows)
        self.toolbar.addWidget(self.exit_button)

        self.setCentralWidget(self.web)

        if not settings["camera_screen"] + 1 > len(QGuiApplication.screens()):
            monitor = QGuiApplication.screens()[settings["camera_screen"]].geometry()
        else:
            monitor = QGuiApplication.screens()[0].geometry()

        self.move(monitor.center())

        if platform.system() == "Windows":
            self.set_windows_dark(settings["dark_mode"])

        if (settings["camera_screen"] > 0 and len(QGuiApplication.screens()) > 1) or (settings["cam_fullscreen"]):
            self.showFullScreen()
        else:
            self.show()

    def set_windows_dark(self, dark: bool):
        if platform.system() == "Windows":
            windll.LoadLibrary("dwmapi").DwmSetWindowAttribute(int(self.winId()), 20, byref(c_bool(dark)), sizeof(BOOL))

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        update_setting("cam_fullscreen", self.isFullScreen())


class FirstRun(QMainWindow):
    def __init__(self):
        super(FirstRun, self).__init__()

        self.setWindowTitle(strings.FIRST_RUN_WINDOW_TITLE)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/icons/icon.svg")))

        self.root_widget = QWidget()
        self.setCentralWidget(self.root_widget)

        self.root_layout = QVBoxLayout()
        self.root_widget.setLayout(self.root_layout)

        self.welcome = QLabel(strings.WELCOME)
        self.welcome.setProperty('class', 'big_title')
        self.welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root_layout.addWidget(self.welcome)

        self.welcome_det = QLabel(strings.WELCOME_DET.format(__version__))
        self.welcome_det.setProperty('class', 'welcome_det')
        self.welcome_det.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root_layout.addWidget(self.welcome_det)

        self.root_layout.addStretch()

        self.first_time_text = QLabel(strings.FIRST_TIME)
        self.first_time_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root_layout.addWidget(self.first_time_text)

        self.root_layout.addStretch()

        self.button_layout = QHBoxLayout()
        self.root_layout.addLayout(self.button_layout)

        self.button_layout.addStretch()

        self.restart = QPushButton(strings.CLOSE)
        self.restart.clicked.connect(self.close)
        self.button_layout.addWidget(self.restart)

        self.tutorial = QPushButton(strings.TAKE_TUTORIAL)
        # self.button_layout.addWidget(self.tutorial)

        if platform.system() == "Windows":
            self.set_windows_dark(settings["dark_mode"])

        self.show()

    def set_windows_dark(self, dark: bool):
        if platform.system() == "Windows":
            windll.LoadLibrary("dwmapi").DwmSetWindowAttribute(int(self.winId()), 20, byref(c_bool(dark)), sizeof(BOOL))


if __name__ == "__main__":
    # settings
    if os.path.exists(args.settings):
        with open(args.settings, encoding="UTF-8") as f:
            settings = json.load(f)
    else:
        settings = DEFAULT_SETTINGS
        save_settings()

    # logging
    logging.basicConfig(level=settings["log_level"])
    logging.debug(f"Loaded settings from {args.settings}")

    # NT
    if not settings["first_run"]:
        NetworkTables.initialize(server=settings["ip"])
        sd = NetworkTables.getTable("SmartDashboard")
        color = NetworkTables.getTable("RevColorSensor_V3")
        sd.addEntryListener(value_changed)  # has to be done after setting up window
        color.addEntryListener(color_value_changed)  # has to be done after setting up window

    # Qt Application
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(strings.APP_NAME)
    app.setApplicationDisplayName(strings.APP_NAME)

    # Theme Setup
    if settings["dark_mode"]:
        qt_material.apply_stylesheet(app, theme="dark_red.xml", css_file="material-fixes.qss")
    else:
        qt_material.apply_stylesheet(app, theme="light_red.xml", css_file="material-fixes.qss")

    # Windows
    if settings["first_run"]:
        settings["first_run"] = False
        save_settings()

        cam = None
        window = None
        fr = FirstRun()
    else:
        cam = CamMonitor()
        window = MainWindow()

    sys.exit(app.exec())
