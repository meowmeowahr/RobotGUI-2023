import PyInstaller.__main__
import os


def build():
    PyInstaller.__main__.run([os.path.join(os.path.dirname(os.path.realpath(__file__)), "robotgui.spec")])


if __name__ == "__main__":
    build()
