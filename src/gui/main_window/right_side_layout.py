"""Layout of the right side of MainWindow of the GUI."""

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

from typing import TYPE_CHECKING

import pyqtgraph as pg
from PyQt6.QtWidgets import QComboBox, QVBoxLayout

if TYPE_CHECKING:
    from src.gui.main_window.main_window import MainWindow


class MainWindowLayoutRightSide(QVBoxLayout):
    """MainWindow right side layout."""

    def __init__(self, main_window: "MainWindow") -> None:
        """Initialize MainWindow right side layout."""
        super().__init__()
        self.cb_plot_type = QComboBox()
        self.cb_plot_type.addItems(["Auto", "String", "Array1D", "Array2D", "ImageRGB", "Table"])
        self.cb_plot_type.currentTextChanged.connect(main_window.handle_plot_type_changed)

        self.plot_wgt_dataset = pg.PlotWidget()

        self.addWidget(self.cb_plot_type)
        self.addWidget(self.plot_wgt_dataset)
