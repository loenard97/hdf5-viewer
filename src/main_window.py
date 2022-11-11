import os
import h5py
import numpy as np
import pyqtgraph as pg

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QSplitter, QTableView

from src.table_model import TableModel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.WindowType.Window)

        # Appearance
        self.setGeometry(300, 150, 1400, 700)
        self.setWindowTitle("HDF5 File Viewer")
        self.setWindowIcon(QIcon(os.path.join("img", "file.svg")))

        # Layout Right Side
        self._table_model = TableModel(header=['Attribute', 'Value'])
        self._table_view = QTableView()
        self._table_view.setModel(self._table_model)
        self._plot_widget = pg.PlotWidget()
        widget_right = QSplitter()
        widget_right.addWidget(self._table_view)
        widget_right.addWidget(self._plot_widget)
        widget_right.setOrientation(Qt.Orientation.Vertical)

        # Center Layout
        self._tree_widget = QTreeWidget()
        self._tree_widget.setColumnCount(2)
        self._tree_widget.setHeaderLabels(["Name", "Type"])
        self._tree_widget.currentItemChanged.connect(self._handle_item_changed)
        central_widget = QSplitter()
        central_widget.addWidget(self._tree_widget)
        central_widget.addWidget(widget_right)
        self.setCentralWidget(central_widget)

        # File Menu
        action_open_file = QAction('&Open File...', self)
        action_open_file.setShortcut('Ctrl+O')
        action_open_file.triggered.connect(self._handle_action_open_file)
        self.menuBar().addMenu('&File').addAction(action_open_file)

        self.show()

    def _tree_recursion(self, item, path):
        """
        Get Array of all Parents
        """
        try:
            path.append(item.parent().text(0))
            self._tree_recursion(item.parent(), path)
        except AttributeError:
            return

    def _hdf5_recursion(self, hdf5_object, root, parent):
        """
        Recursively go through hdf5 File and construct QTreeWidgetItems
        """
        for name, value in hdf5_object.items():
            if str(type(value)) == "<class 'h5py._hl.group.Group'>":
                child_item = QTreeWidgetItem(parent, type=0)
                child_item.setText(0, name)
                child_item.setText(1, "Group")
                child_item.setIcon(1, QIcon(os.path.join("img", "group.png")))
                parent.addChild(child_item)
                self._hdf5_recursion(value, root, child_item)

            elif str(type(value)) == "<class 'h5py._hl.dataset.Dataset'>":
                child_item = QTreeWidgetItem(parent, type=0)
                child_item.setText(0, name)
                child_item.setText(1, "Dataset")
                child_item.setIcon(1, QIcon(os.path.join("img", "dataset.png")))
                parent.addChild(child_item)

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def _handle_item_changed(self, current, _):
        """
        Update Info of currently selected Item
        """
        parents_list = [current.text(0)]
        self._tree_recursion(current, parents_list)
        parents_list.reverse()

        if len(parents_list) == 1:
            # Selected Item is a File
            self._table_model.resetData()
            self._table_model.appendRow(["Name", parents_list[0]])
            self._plot_widget.clear()

        else:
            with h5py.File(parents_list[0], 'r') as file:
                path = ''
                for e in parents_list[1:]:
                    path += '/' + e
                h5_obj = file[path]

                if str(type(h5_obj)) == "<class 'h5py._hl.group.Group'>":
                    # Selected Item is a Group
                    self._table_model.resetData()
                    self._table_model.appendRow(["Name", str(h5_obj.name)])
                    self._plot_widget.clear()

                elif str(type(h5_obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                    # Selected Item is a Dataset
                    data = np.array(h5_obj)

                    self._table_model.resetData()
                    self._table_model.appendRow(["Name", str(h5_obj.name)])
                    self._table_model.appendRow(["Size", str(h5_obj.size)])
                    self._table_model.appendRow(["Shape", str(h5_obj.shape)])
                    self._table_model.appendRow(["Dimensions", str(h5_obj.ndim)])
                    self._table_model.appendRow(["Data Type", str(h5_obj.dtype)])
                    self._table_model.appendRow(["Data", np.array_str(data)])

                    self._plot_widget.clear()
                    try:
                        self._plot_widget.plot(data)
                    except Exception as err:
                        print(f"could not plot {err}")

    @pyqtSlot()
    def _handle_action_open_file(self):
        """
        Open HDF5 File
        """
        # Get File Name
        hdf5_path, _ = QFileDialog.getOpenFileName(
            self, 'Open file', os.getcwd(), "HDF5 File (*.hdf5);;All Files (*.*)")

        # Load TreeView from File
        with h5py.File(hdf5_path, 'r') as file:
            parent_item = QTreeWidgetItem()
            parent_item.setText(0, hdf5_path)
            parent_item.setText(1, "HDF5 File")
            parent_item.setIcon(1, QIcon(os.path.join("img", "file.svg")))
            self._hdf5_recursion(hdf5_object=file, root=parent_item, parent=parent_item)
            self._tree_widget.insertTopLevelItems(0, [parent_item])
