"""Children of QAbstractTableModel."""

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

from typing import Any

import numpy.typing as npt
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    """Table Model that can append and remove Rows."""

    def __init__(self, header: list[str]) -> None:
        """Table Model that can append and remove Rows."""
        QAbstractTableModel.__init__(self)
        self._header = header
        self._data: list[Any] = []

    def rowCount(self, parent: None | QModelIndex = None) -> int:
        """Get Row Count."""
        return len(self._data)

    def columnCount(self, parent: None | QModelIndex = None) -> int:
        """Get Column Count."""
        return len(self._header)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Item Flags for Cell at Index."""
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def appendRow(self, new_data: list[Any]) -> bool:
        """Append Row."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(new_data)
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent: None | QModelIndex = None) -> bool:
        """Remove Row."""
        self.beginRemoveRows(QModelIndex(), row, row)
        try:
            self._data.pop(row)
        except IndexError:
            self.endRemoveRows()
            return False
        self.endRemoveRows()
        return True

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Get Data, Alignment, Colors etc. depending on Role."""
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(
        self, index: QModelIndex, value: str, role: int = Qt.ItemDataRole.EditRole
    ) -> bool:
        """Set Data when Cell is edited."""
        if role != Qt.ItemDataRole.EditRole:
            return False

        self._data[index.row()][index.column()] = value
        self.dataChanged.emit(index, index)
        return True

    def getData(self, index: Any = None) -> Any:
        """Get Data at Index or Row."""
        if index is None:
            return self._data
        elif isinstance(index, QModelIndex):
            return self._data[index.row()][index.column()]
        elif isinstance(index, int):
            return self._data[index]

    def resetData(self) -> None:
        """Reset to Empty Table."""
        for i in range(self.rowCount()):
            self.removeRow(0)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> None | str | int:
        """Get Headers for horizontal | vertical Orientation."""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._header[section]
            if orientation == Qt.Orientation.Vertical:
                return section + 1
        return None


class DataTable(QAbstractTableModel):
    """Table Model for 2D Numpy Arrays."""

    def __init__(self, data: npt.NDArray) -> None:
        """Table Model for 2D Numpy Arrays."""
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent: None | QModelIndex = None) -> int:
        """Get Row Count."""
        return int(self._data.shape[0])

    def columnCount(self, parent: None | QModelIndex = None) -> int:
        """Get Column Count."""
        return int(self._data.shape[1])

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> None | float:
        """Get Data, Alignment, Colors etc. depending on Role."""
        if role == Qt.ItemDataRole.DisplayRole:
            return float(self._data[index.row()][index.column()])
        return None
