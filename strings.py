""" Strings for RobotGUI """

# strings.py Settings
from typing import Final

ENABLE_TUTORIAL: Final[bool] = False

# Main
APP_NAME = "RobotGUI"

ROBOT_NAME_EE = bytes.fromhex("f09f908820456c204761746f204c6f636f20f09f9088").decode("utf-8")

CONN_NOT_CONNECTED = "{0} does not have an active NetworkTables server."

MENU_FILE = "File"
MENU_HELP = "Help"
MENU_ABOUT = "About"
MENU_ABOUT_QT = "About Qt"
MENU_SETUP = "Settings"
MENU_QUIT = "Quit"

TAB_OBJECT = "Operator Status"
TAB_COLOR = "Color Sensor"
TAB_SWERVE = "Swerve"

TAB_SWERVE_CHILD_0 = "Mod 0"

LABEL_CANCODER_TITLE = "Cancoder"
LABEL_INTEGRATED_TITLE = "Intergrated"
LABEL_VELOCITY_TITLE = "Velocity"

SWERVE_MOD = "Swerve Mod {0}"

# Settings
SETUP_WINDOW_TITLE = "Settings"

TAB_SETUP_THEME = "Theme"
TAB_SETUP_CONNS = "Connection"
TAB_SETUP_CAM = "Camera"

LABEL_CONNS_WARNING = "Restart the application for these settings to apply"
LABEL_CAM_WARNING = "Restart the application for these settings to apply"

CHECK_DARK_MODE = "Dark Mode"

EDIT_SETUP_IP = "IP Address"
EDIT_SETUP_IP_PLHOLD = "10.XX.XX.X"

EDIT_SETUP_CAM = "Camera Address"
EDIT_SETUP_CAM_PLHOLD = "Camera HTTP Link"

SPIN_CAM_SCREEN = "Default Camera Display"

# Cams
CAM_TITLE = "Camera Stream"

CAM_TOOLBAR = "Camera Browser Toolbar"

# First Run
FIRST_RUN_WINDOW_TITLE = "First Run"

WELCOME = "Welcome to RobotGUI!"
WELCOME_DET = "It looks like this is the first time running RobotGUI v{0}"

TAKE_TUTORIAL = "Take the Tutorial"

FIRST_TIME = f"{'Take the tutorial or r' if ENABLE_TUTORIAL else 'R'}estart the app to start NetworkTables"

# Misc
UNKNOWN = "Unknown"

CLOSE = "Close"


if __name__ == "__main__":
    print("This file is not meant to be run directly")
