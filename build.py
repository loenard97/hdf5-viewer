import os
import sys

import PyInstaller.__main__


def build():
    version = "v1.0"
    if sys.platform == 'win32':
        out_name = "main.exe"
        file_name = os.path.join("dist", f"HDF5Viewer_Win32_{version}.exe")
    elif sys.platform == 'linux':
        out_name = "main"
        file_name = os.path.join("dist", f"HDF5Viewer_Linux_{version}")
    else:
        raise OSError

    if os.path.exists(file_name):
        os.remove(file_name)
    PyInstaller.__main__.run([
        'main.py',
        '--noconfirm',
        '--windowed'
    ])
    # os.rename(out_name, file_name)


if __name__ == '__main__':
    build()
