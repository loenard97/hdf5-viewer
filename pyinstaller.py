import os
import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        "hdf5viewer.py",
        "--noconfirm",
        "--windowed",
        "--icon=img/file.svg",
        "--add-data=img/*" + os.pathsep + "img",
        "--add-data=html/*" + os.pathsep + "html",
        "--add-data=LICENSE" + os.pathsep + ".",
        "--add-data=README.md" + os.pathsep + ".",
    ])


if __name__ == '__main__':
    build()
