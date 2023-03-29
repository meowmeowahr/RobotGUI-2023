""" Strings for RobotGUI """

# Main
WINDOW_TITLE = "RobotGUI"

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

# Settings
SETUP_WINDOW_TITLE = "Settings"

TAB_SETUP_THEME = "Theme"
TAB_SETUP_CONNS = "Connection"

LABEL_CONNS_WARNING = "Restart the application to these settings to apply"

CHECK_DARK_MODE = "Dark Mode"

EDIT_SETUP_IP = "IP Address"
EDIT_SETUP_IP_PLHOLD = "XX.XX.XX.XX"

EDIT_SETUP_CAM = "Camera Address"
EDIT_SETUP_CAM_PLHOLD = "Camera HTTP Link"

# Cams
CAM_TITLE = "Camera Stream"

CAM_TOOLBAR = "Camera Browser Toolbar"


if __name__ == "__main__":
    print("This file is not meant to be run directly")
