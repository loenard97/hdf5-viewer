"""QWidgets that plot 2D numpy arrays as table."""

from typing import override

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
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWidgets import QTableView


class DataWidget2DTable(QTableView):
    """Data Table View."""

    def __init__(self, data: npt.NDArray) -> None:
        """Initialize Data Table View."""
        super().__init__()

        model = DataTableModel(data)
        self.setModel(model)


class DataTableModel(QAbstractTableModel):
    """Table Model for 2D Numpy Arrays."""

    def __init__(self, data: npt.NDArray) -> None:
        """Table Model for 2D Numpy Arrays."""
        QAbstractTableModel.__init__(self)
        self._data = data

    @override
    def rowCount(self, _: None | QModelIndex = None) -> int:
        """Get Row Count."""
        return int(self._data.shape[0])

    @override
    def columnCount(self, _: None | QModelIndex = None) -> int:
        """Get Column Count."""
        return int(self._data.shape[1])

    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> None | float:
        """Get Data, Alignment, Colors etc. depending on Role."""
        if role == Qt.ItemDataRole.DisplayRole:
            return float(self._data[index.row()][index.column()])

        return None
