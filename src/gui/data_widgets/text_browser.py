"""QWidgets that plot string data as text browsers."""

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

import pathlib

import numpy.typing as npt
from natsort import natsorted
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QTextBrowser


class DataWidgetText(QTextBrowser):
    """QTextBrowser that plots string data of a numpy array."""

    def __init__(self, data: npt.NDArray) -> None:
        """Initialize Data Text Browser."""
        super().__init__()
        if data.ndim == 0:
            label = data.item()
            if isinstance(label, bytes):
                label = label.decode()
            label = str(label)
        else:
            label = str(data)
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)


class DataWidgetFileText(QTextBrowser):
    """QTextBrowser that plots string data of an HDF5 file."""

    def __init__(self, data: pathlib.Path) -> None:
        """File Text Browser."""
        super().__init__()
        label = "HDF5 File (" + self.file_size_to_str(data) + "):\n" + str(data)
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)

    @staticmethod
    def file_size_to_str(file_path: pathlib.Path) -> str:
        """Get file size as formatted string."""
        size = file_path.stat().st_size
        kilo_byte = 1024

        if size > kilo_byte**3:
            return f"{size / kilo_byte**3:.2f} GB"
        if size > kilo_byte**2:
            return f"{size / kilo_byte**2:.2f} MB"
        if size > kilo_byte:
            return f"{size / kilo_byte:.2f} kB"
        return f"{size} bytes"


class DataWidgetGroupText(QTextBrowser):
    """QTextBrowser that plots string data of an HDF5 group."""

    def __init__(self, data: npt.NDArray) -> None:
        """Group Text Browser."""
        super().__init__()
        label = "Group:\n" + "\n".join(f" - {e}" for e in natsorted(data))
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)
