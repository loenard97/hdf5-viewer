import os
from sys import platform
import PyInstaller.__main__


def build():
    is_windows = platform == "win32"
    PyInstaller.__main__.run([
        "src/hdf5viewer/main.py",
        "--noconfirm",
        "--windowed",
        f"--icon=src/hdf5viewer/img/file.{'ico' if is_windows else 'svg'}",
        "--add-data=src/hdf5viewer/img/*" + os.pathsep + "img",
        "--add-data=src/hdf5viewer/html/*" + os.pathsep + "html",
        "--add-data=LICENSE" + os.pathsep + ".",
        "--add-data=README.md" + os.pathsep + ".",
    ])


if __name__ == '__main__':
    build()
