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

import pyqtgraph
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QPalette
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
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 246))
    palette.setColor(QPalette.ColorRole.WindowText, QColor.fromString("black"))
    palette.setColor(QPalette.ColorRole.Base, QColor(219, 223, 229))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(219, 223, 229))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor.fromString("black"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor.fromString("black"))
    palette.setColor(QPalette.ColorRole.Text, QColor.fromString("black"))
    palette.setColor(QPalette.ColorRole.Button, QColor(219, 223, 229))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor.fromString("black"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor.fromString("red"))

    palette.setColor(QPalette.ColorRole.Highlight, QColor(112, 175, 234))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor.fromString("black"))

    with open("styles/style.css", "r") as file:
        css = file.read()

    pyqtgraph.setPalette(app, palette)
    app.setPalette(palette)
    app.setStyleSheet(css)

    # Load font from file
    font_id = QFontDatabase.addApplicationFont("fonts/NotoSans/NotoSans-Regular.ttf")
    if font_id < 0:
        print("Failed to load font!")
    else:
        families = QFontDatabase.applicationFontFamilies(font_id)
        print("Loaded font families:", families)
        # Use the first family name
        edwin_font = QFont(families[0], 10)
        app.setFont(edwin_font)

    app.setOrganizationName("HDF5Viewer")
    app.setApplicationName("HDF5ViewerPython")
    main_win = MainWindow()
    main_win.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
