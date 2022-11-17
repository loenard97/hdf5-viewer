import os
import h5py
import numpy as np
import pyqtgraph as pg

from PyQt6.QtCore import Qt, pyqtSlot, QAbstractTableModel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QSplitter, QTableView, QFormLayout, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel

from src.table_model import TableModel, DataTable
from src.tree_widget import FileTreeWidget


class MainWindow(QMainWindow):

    def __init__(self, init_file_path):
        super().__init__(flags=Qt.WindowType.Window)

        self._curr_file = None
        self._curr_obj_path = None

        # Appearance
        self.setGeometry(300, 150, 1400, 700)
        self.setWindowTitle("HDF5 File Viewer")
        self.setWindowIcon(QIcon(os.path.join("img", "file.svg")))

        # Layout Right Side
        self._table_model = TableModel(header=['Attribute', 'Value'])
        self._table_view = QTableView()
        self._table_view.setModel(self._table_model)
        form_layout = QFormLayout()
        self._plot_selection = QComboBox()
        self._plot_selection.addItems(["Auto", "None", "Text", "1D Plot", "Table", "2D Image", "2D RGB Image"])
        self._plot_selection.currentTextChanged.connect(self._handle_plot_changed)
        form_layout.addRow("Show Dataset as", self._plot_selection)
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self._plot_widget = pg.PlotWidget()
        self._layout_right = QVBoxLayout()
        self._layout_right.addWidget(self._table_view)
        self._layout_right.addWidget(form_widget)
        self._layout_right.addWidget(self._plot_widget)

        # Center Layout
        self._tree_widget = FileTreeWidget(self)
        self._tree_widget.setColumnCount(2)
        self._tree_widget.setHeaderLabels(["Name", "Type"])
        self._tree_widget.setAcceptDrops(True)
        self._tree_widget.currentItemChanged.connect(self._handle_item_changed)
        central_widget = QHBoxLayout()
        central_widget.addWidget(self._tree_widget)
        central_widget.addLayout(self._layout_right)
        widget = QWidget()
        widget.setLayout(central_widget)
        self.setCentralWidget(widget)

        # File Menu
        action_open_file = QAction('&Open File...', self)
        action_open_file.setShortcut('Ctrl+O')
        action_open_file.triggered.connect(self._handle_action_open_file)
        self.menuBar().addMenu('&File').addAction(action_open_file)

        self.show()

        if init_file_path is not None:
            self.open_file(init_file_path)

    def open_file(self, file_path):
        """
        Open one File
        """
        try:
            # Load TreeView from File
            with h5py.File(file_path, 'r') as file:
                print(f"Open '{file_path}'")
                parent_item = QTreeWidgetItem()
                parent_item.setText(0, file_path)
                parent_item.setText(1, "HDF5 File")
                parent_item.setIcon(1, QIcon(os.path.join("img", "file.svg")))
                self._hdf5_recursion(hdf5_object=file, root=parent_item, parent=parent_item)
                self._tree_widget.insertTopLevelItems(0, [parent_item])
        except (OSError, ValueError):
            print(f"Failed to open '{file_path}'")

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

    def _plot_data(self):
        """
        Update Plot
        """
        text = self._plot_selection.currentText()
        print(f"Update Plot to {text}")

        if self._curr_file is None or self._curr_obj_path is None or not os.path.exists(self._curr_file):
            data = np.array([])
        else:
            with h5py.File(self._curr_file, 'r') as file:
                data = np.array(file[self._curr_obj_path])
                print(data.shape, data.size)

        if text == "None":
            new_widget = QWidget()
        
        elif text == "Auto":
            new_widget = QLabel("Undefined Option")

        elif text == "Text":
            try:
                label = str(data)
            except:
                new_widget = QLabel("Could not convert Dataset to Text")
            if len(label) > 1000:
                label = label[:1000] + '...'
            new_widget = QLabel(label)

        elif text == "1D Plot":
            if len(data.shape) == 1:
                new_widget = pg.PlotWidget()
                try:
                    new_widget.plot(data)
                except:
                    print("Could not plot")
            else:
                new_widget = QLabel("Dataset is not 1D")
        
        elif text == "2D Image":
            if len(data.shape) == 2:
                new_widget = pg.ImageView()
                new_widget.setImage(data)
                new_widget.setColorMap(pg.colormap.get("inferno"))
            else:
                new_widget = QLabel("Dataset is not 2D")

        elif text == "2D RGB Image":
            if len(data.shape) == 3 and data.shape[0] == 3:
                data = np.sum(data, axis=0)
                print(data.shape)
                new_widget = pg.ImageView()
                new_widget.setImage(data)
                new_widget.setColorMap(pg.colormap.get("inferno"))
            else:
                new_widget = QLabel("Dataset is not a 2D RGB Image")
        
        elif text == "Table":
            if len(data.shape) <= 2 and data.size < 100:
                new_widget = QTableView()
                model = DataTable(data)
                new_widget.setModel(model)
            else:
                new_widget = QLabel("Dataset is not 2D or is to large for Table")

        else:
            new_widget = QLabel("Undefined Option")

        self._layout_right.replaceWidget(self._plot_widget, new_widget)
        self._plot_widget.hide()
        self._plot_widget.destroy()
        self._plot_widget = new_widget

    # ----- Slots -----
    @pyqtSlot(str)
    def _handle_plot_changed(self, text):
        """
        Change current Plot
        """
        print(f"Change Plot to {text}")
        print(self._curr_file)
        print(self._curr_obj_path)
        self._plot_data()

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def _handle_item_changed(self, current, _):
        """
        Update Info of currently selected Item
        """
        parents_list = [current.text(0)]
        self._tree_recursion(current, parents_list)
        parents_list.reverse()
        path = ''
        for e in parents_list[1:]:
            path += '/' + e
        self._curr_file = parents_list[0]
        self._curr_obj_path = path

        if len(parents_list) == 1:
            # Selected Item is a File
            self._table_model.resetData()
            self._table_model.appendRow(["Name", parents_list[0]])
            return

        with h5py.File(parents_list[0], 'r') as file:
            h5_obj = file[path]

            if str(type(h5_obj)) == "<class 'h5py._hl.group.Group'>":
                # Selected Item is a Group
                self._table_model.resetData()
                self._table_model.appendRow(["Name", str(h5_obj.name)])

            elif str(type(h5_obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                # Selected Item is a Dataset
                self._table_model.resetData()
                self._table_model.appendRow(["Name", str(h5_obj.name)])
                self._table_model.appendRow(["Size", str(h5_obj.size)])
                self._table_model.appendRow(["Shape", str(h5_obj.shape)])
                self._table_model.appendRow(["Dimensions", str(h5_obj.ndim)])
                self._table_model.appendRow(["Data Type", str(h5_obj.dtype)])
        
        self._plot_data()

    @pyqtSlot()
    def _handle_action_open_file(self):
        """
        Open HDF5 File
        """
        # Get File Name
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open file', os.getcwd(), "HDF5 File (*.hdf5, *.h5);;All Files (*.*)")
        self.open_file(file_path)
