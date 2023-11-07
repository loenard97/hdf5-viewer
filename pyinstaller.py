"""Build executable with pyinstaller."""

# Copyright (C) 2023 Dennis Lönard
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from sys import platform

import PyInstaller.__main__


def build():
    """Build executable with pyinstaller."""
    is_windows = platform == "win32"
    PyInstaller.__main__.run(
        [
            "main.py",
            "--noconfirm",
            "--windowed",
            f"--icon=src/img/file.{'ico' if is_windows else 'svg'}",
            "--add-data=src/img/*" + os.pathsep + "img",
            "--add-data=src/html/*" + os.pathsep + "html",
            "--add-data=LICENSE" + os.pathsep + ".",
            "--add-data=README.md" + os.pathsep + ".",
        ]
    )


if __name__ == "__main__":
    build()
