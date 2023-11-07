"""HDF5 File Viewer entry point."""

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

import logging
import os
import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from hdf5viewer.gui.main_window import MainWindow

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("hdf5viewer")

if "--debug" in sys.argv:
    logging.basicConfig(
        level=0,
        format="%(asctime)s: [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("hdf5viewer.log")),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )
else:
    logging.basicConfig(
        level=20,
        format="%(asctime)s: [%(levelname)s] - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def main() -> None:
    """HDF5 File Viewer entry point."""
    if len(sys.argv) > 1:
        file_path = pathlib.Path(sys.argv[1])
    else:
        file_path = pathlib.Path("")

    app = QApplication(sys.argv)
    app.setOrganizationName("HDF5Viewer")
    app.setApplicationName("HDF5ViewerPython")
    main_win = MainWindow(init_file_path=file_path)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
