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

import sys

import PyInstaller.__main__


def build() -> None:
    """Build executable with pyinstaller."""
    build_args = [
        "main.py",
        "--noconfirm",
        "--windowed",
        "--add-data=src/img/*:img",
        "--add-data=src/html/*:html",
        "--add-data=LICENSE:.",
        "--add-data=README.md:.",
    ]
    if sys.platform == "win32":
        build_args.append("--icon=src/img/file.ico")
    else:
        build_args.append("--onefile")

    PyInstaller.__main__.run(build_args)


if __name__ == "__main__":
    build()
