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

import logging.config
import sys

from PyQt6.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.logging_config import logging_config

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("hdf5viewer")


def main() -> None:
    """HDF5 File Viewer entry point."""
    logging.config.dictConfig(logging_config)
    logging.info("Starting GUI...")

    app = QApplication(sys.argv)
    app.setOrganizationName("HDF5Viewer")
    app.setApplicationName("HDF5ViewerPython")
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
