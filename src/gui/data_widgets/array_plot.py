"""QWidgets that plot 1D numpy arrays."""

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

import numpy.typing as npt
import pyqtgraph as pg


class DataWidget1DArray(pg.PlotWidget):
    """pg.PlotWidget that plots a 1D numpy array."""

    def __init__(self, data: npt.NDArray) -> None:
        """Initialize Array Plot Widget."""
        super().__init__()
        unravel_dimension = 2
        if data.ndim == unravel_dimension and min(data.shape) == 1:
            data = data.ravel()
        self.plot(data, pen="black")
