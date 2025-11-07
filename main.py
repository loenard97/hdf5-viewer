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
import pathlib
import sys

import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

from src.config.font import create_font
from src.config.logging import create_logging_config
from src.config.palette import create_color_palette
from src.gui.main_window.main_window import MainWindow

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("hdf5viewer")


def main() -> None:
    """HDF5 File Viewer entry point."""
    logging_config = create_logging_config()
    logging.config.dictConfig(logging_config)

    app = QApplication(sys.argv)  # QApplication has to be created before palette and font are created

    palette = create_color_palette()
    font = create_font()
    with pathlib.Path("styles/style.css").open() as file:
        style_sheet = file.read()

    app.setOrganizationName("HDF5Viewer")
    app.setApplicationName("HDF5 File Viewer")
    app.setStyle("Fusion")
    app.setPalette(palette)
    app.setStyleSheet(style_sheet)
    app.setFont(font)

    pg.setPalette(app, palette)
    pg.setConfigOption(opt="background", value="#dbdfe5")
    pg.setConfigOption(opt="foreground", value="#000000")
    pg.setConfigOption(opt="antialias", value=True)

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
