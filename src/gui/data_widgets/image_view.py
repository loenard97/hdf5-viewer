"""QWidgets that plot 2D numpy arrays as image."""

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

import numpy as np
import numpy.typing as npt
import pyqtgraph as pg


class DataWidget2DImage(pg.ImageView):
    """Data Image View."""

    def __init__(self, data: npt.NDArray) -> None:
        """Initialize Data Image View."""
        super().__init__()

        self.setImage(data)
        self.setColorMap(pg.colormap.get("inferno"))


class DataWidget3DRGBImage(pg.ImageView):
    """Data Image RGB View."""

    def __init__(self, data: npt.NDArray) -> None:
        """Initialize Data Image RGB View."""
        super().__init__()

        data = np.sum(data, axis=0)
        self.setImage(data)
        self.setColorMap(pg.colormap.get("inferno"))
