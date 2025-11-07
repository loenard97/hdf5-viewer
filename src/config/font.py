"""Font configs."""

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

from PyQt6.QtGui import QFont, QFontDatabase


def create_font() -> QFont:
    """Create font used for the QApplication."""
    font_size = 10
    font_id = QFontDatabase.addApplicationFont("fonts/NotoSans/NotoSans-Regular.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    return QFont(font_families[0], font_size)
