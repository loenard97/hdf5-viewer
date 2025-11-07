"""Color palettes."""

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

from PyQt6.QtGui import QColor, QPalette


def create_color_palette() -> QPalette:
    """Create QPalette used for the QApplication."""
    color_black = QColor.fromString("black")
    color_red = QColor.fromString("red")
    color_blue = QColor(112, 175, 234)
    color_gray = QColor(219, 223, 229)
    color_bright_gray = QColor(245, 245, 246)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, color_bright_gray)
    palette.setColor(QPalette.ColorRole.WindowText, color_black)
    palette.setColor(QPalette.ColorRole.Base, color_gray)
    palette.setColor(QPalette.ColorRole.AlternateBase, color_gray)
    palette.setColor(QPalette.ColorRole.ToolTipBase, color_black)
    palette.setColor(QPalette.ColorRole.ToolTipText, color_black)
    palette.setColor(QPalette.ColorRole.Text, color_black)
    palette.setColor(QPalette.ColorRole.Button, color_gray)
    palette.setColor(QPalette.ColorRole.ButtonText, color_black)
    palette.setColor(QPalette.ColorRole.BrightText, color_red)
    palette.setColor(QPalette.ColorRole.Highlight, color_blue)
    palette.setColor(QPalette.ColorRole.HighlightedText, color_black)

    return palette
