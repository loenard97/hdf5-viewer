import os
import sys

import PyInstaller.__main__


def build():
    version = "v1.0"
    if sys.platform == 'win32':
        file_name = os.path.join("dist", f"HDF5Viewer_Win32_{version}.exe")
    elif sys.platform == 'linux':
        file_name = os.path.join("dist", f"HDF5Viewer_Linux_{version}")
    else:
        raise OSError

    if os.path.exists(file_name):
        os.remove(file_name)
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed'
    ])
    os.rename(os.path.join('dist', 'main.exe'), file_name)


if __name__ == '__main__':
    build()
