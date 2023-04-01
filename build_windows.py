import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "robotgui.spec")
])
