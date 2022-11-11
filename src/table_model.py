from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):
    """
    Table Model that asserts correct Data Types for each Row.
    """

    def __init__(self, header):
        QAbstractTableModel.__init__(self)
        self._header = header
        self._data = []

    def rowCount(self, parent=None) -> int:
        """
        Get Row Count
        """
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        """
        Get Column Count
        """
        return len(self._header)

    def flags(self, index: QModelIndex):
        """
        Item Flags for Cell at Index
        """
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def appendRow(self, new_data: list) -> bool:
        """
        Append Row
        """
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(new_data)
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent=QModelIndex()) -> bool:
        """
        Remove Row
        """
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.pop(row)
        self.endRemoveRows()
        return True

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        """
        Get Data, Alignment, Colors etc. depending on Role
        """
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index: QModelIndex, value: str, role=Qt.ItemDataRole.EditRole) -> bool:
        """
        Set Data when Cell is edited
        """
        if role != Qt.ItemDataRole.EditRole:
            return False

        self._data[index.row()][index.column()] = value
        self.dataChanged.emit(index, index)
        return True

    def getData(self, index=None):
        """
        Get Data at Index or Row
        """
        if index is None:
            return self._data
        elif isinstance(index, QModelIndex):
            return self._data[index.row()][index.column()]
        elif isinstance(index, int):
            return self._data[index]

    def resetData(self):
        """
        Reset to Empty Table
        """
        for i in range(self.rowCount()):
            self.removeRow(0)

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Get Headers for horizontal | vertical Orientation
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._header[section]
            if orientation == Qt.Orientation.Vertical:
                return section + 1
        return None
