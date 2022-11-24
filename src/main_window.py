import os
import h5py
import numpy as np
import pyqtgraph as pg

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QIcon, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QTableView, QFormLayout, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeWidget, QMessageBox

from src.static_functions import file_size_to_str
from src.table_model import TableModel, DataTable


class MainWindow(QMainWindow):

    def __init__(self, init_file_path):
        super().__init__(flags=Qt.WindowType.Window)
        self.setAcceptDrops(True)

        # Variables
        self._curr_file = None
        self._curr_obj_path = None

        # Appearance
        self.setGeometry(300, 150, 1400, 700)
        self.setWindowTitle("HDF5 Viewer")
        self.setWindowIcon(QIcon(os.path.join("img", "h5.svg")))

        # Layout Right Side
        self._table_model = TableModel(header=['Attribute', 'Value'])
        self._table_view = QTableView()
        self._table_view.setModel(self._table_model)
        form_layout = QFormLayout()
        self._plot_selection = QComboBox()
        self._plot_selection.addItems(["None", "Text", "1D Plot", "Table", "2D Image", "2D RGB Image"])
        self._plot_selection.setCurrentText("1D Plot")
        self._plot_selection.currentTextChanged.connect(self._plot_data)
        form_layout.addRow("Show Dataset as", self._plot_selection)
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self._plot_widget = pg.PlotWidget()
        self._layout_right = QVBoxLayout()
        self._layout_right.addWidget(self._table_view)
        self._layout_right.addWidget(form_widget)
        self._layout_right.addWidget(self._plot_widget)

        # Center Layout
        self._tree_widget = QTreeWidget(self)
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
        file_menu = self.menuBar().addMenu("&File")

        action_open_file = QAction('&Open File...', self)
        action_open_file.setShortcut('Ctrl+O')
        action_open_file.triggered.connect(self._handle_action_open_file)
        file_menu.addAction(action_open_file)

        action_open_folder = QAction('&Open Folder...', self)
        action_open_folder.triggered.connect(self._handle_action_open_folder)
        file_menu.addAction(action_open_folder)

        action_clear_files = QAction('&Clear all Files', self)
        action_clear_files.triggered.connect(self._handle_action_clear_files)
        file_menu.addAction(action_clear_files)

        file_menu.addSeparator()

        action_quit = QAction("&Quit", self)
        action_quit.setShortcut("Ctrl+Q")
        action_quit.triggered.connect(self.close)
        file_menu.addAction(action_quit)
        
        # Export Menu
        export_menu = self.menuBar().addMenu("&Export")
        action_export = QAction('&Export Dataset...', self)
        action_export.setShortcut('Ctrl+E')
        action_export.triggered.connect(self._handle_action_export)
        export_menu.addAction(action_export)


        # Open File when double clicking on it
        if init_file_path is not None:
            self._open_file(init_file_path)

    def _open_file(self, file_path):
        """
        Open one File
        """
        try:
            # Load TreeView from File
            with h5py.File(file_path, 'r') as file:
                parent_item = QTreeWidgetItem()
                parent_item.setText(0, file_path)
                parent_item.setText(1, "HDF5 File")
                parent_item.setIcon(1, QIcon(os.path.join("img", "h5.svg")))
                self._hdf5_recursion(hdf5_object=file, root=parent_item, parent=parent_item)
                self._tree_widget.insertTopLevelItem(self._tree_widget.topLevelItemCount(), parent_item)
        except (OSError, ValueError):
            pass

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
                # child_item.setIcon(1, QIcon(os.path.join("img", "group.svg")))
                parent.addChild(child_item)
                self._hdf5_recursion(value, root, child_item)

            elif str(type(value)) == "<class 'h5py._hl.dataset.Dataset'>":
                child_item = QTreeWidgetItem(parent, type=0)
                child_item.setText(0, name)
                child_item.setText(1, "Dataset")
                child_item.setIcon(1, QIcon(os.path.join("img", "dataset.svg")))
                parent.addChild(child_item)

    def _plot_data(self):
        """
        Update Plot Widget
        """
        plot_type = self._plot_selection.currentText()

        if self._curr_file is None or self._curr_obj_path is None or not os.path.exists(self._curr_file):
            data = np.array([])
        else:
            with h5py.File(self._curr_file, 'r') as file:
                data = np.array(file[self._curr_obj_path])

        if plot_type == "None":
            new_widget = QWidget()

        elif plot_type == "Text":
            try:
                label = str(data)
            except:
                new_widget = QLabel("Could not convert Dataset to Text")
            if len(label) > 1000:
                label = label[:1000] + '...'
            new_widget = QLabel(label)

        elif plot_type == "1D Plot":
            if len(data.shape) == 1:
                new_widget = pg.PlotWidget()
                try:
                    new_widget.plot(data)
                except:
                    pass
            else:
                new_widget = QLabel("Dataset is not 1D")
        
        elif plot_type == "2D Image":
            if len(data.shape) == 2:
                new_widget = pg.ImageView()
                new_widget.setImage(data)
                new_widget.setColorMap(pg.colormap.get("inferno"))
            else:
                new_widget = QLabel("Dataset is not 2D")

        elif plot_type == "2D RGB Image":
            if len(data.shape) == 3 and data.shape[0] == 3:
                data = np.sum(data, axis=0)
                new_widget = pg.ImageView()
                new_widget.setImage(data)
                new_widget.setColorMap(pg.colormap.get("inferno"))
            else:
                new_widget = QLabel("Dataset is not a 2D RGB Image")
        
        elif plot_type == "Table":
            if len(data.shape) <= 2 and data.size < 100:
                new_widget = QTableView()
                model = DataTable(data)
                new_widget.setModel(model)
            else:
                new_widget = QLabel("Dataset is not 2D or is to large for Table")

        else:
            new_widget = QLabel("Undefined Option")

        # Replace old Plot Widget
        self._layout_right.replaceWidget(self._plot_widget, new_widget)
        self._plot_widget.hide()
        self._plot_widget.destroy()
        self._plot_widget = new_widget

    # ----- Drag & Drop -----
    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Accept Drag Events for h5 and hdf5 files to initiate Drag & Drop Events
        """
        for file in event.mimeData().text().split('\n'):
            if len(file) == 0:
                continue
            if not file.split('.')[-1] in ['h5', 'hdf5']:
                return
        event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """
        Open Files that are dropped into Window
        """
        for file in event.mimeData().text().split('\n'):
            self._open_file(file[8:])
        event.acceptProposedAction()

    # ----- Slots -----
    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def _handle_item_changed(self, current, _):
        """
        Update Info of currently selected Item
        """
        if current is None:
            return

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
            self._table_model.appendRow(["File Size", file_size_to_str(parents_list[0])])
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
        Open HDF5 Files
        """
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open File", os.path.expanduser('~'), "HDF5 File (*.hdf5, *.h5);;All Files (*.*)")
        for file in file_paths:
            self._open_file(file)

    @pyqtSlot()
    def _handle_action_open_folder(self):
        """
        Open all HDF5 Files in a Folder
        """
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", os.path.expanduser('~'))
        if folder_path:
            for file in os.listdir(folder_path):
                self._open_file(os.path.join(folder_path, file))
    
    @pyqtSlot()
    def _handle_action_clear_files(self):
        """
        Clear Tree Widget
        """
        self._tree_widget.clear()
        self._table_model.resetData()

    @pyqtSlot()
    def _handle_action_export(self):
        """
        Export selected Dataset
        """
        # Get Dataset
        try:
            with h5py.File(self._curr_file, 'r') as h5_file:
                dataset = np.array(h5_file[self._curr_obj_path])
        except ValueError:
            QMessageBox.critical(self, "Error", "No Dataset selected")
            return

        # Get File Path
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Dataset", os.path.expanduser('~'), "CSV File (*.csv);;Numpy File (*.npy);;All Files (*.*)")

        # Save File
        file_type = file_path.split('.')[-1]
        if file_type == 'csv':
            np.savetxt(fname=file_path, X=dataset, delimiter=',', newline='\n', fmt='%.0f')
        
        elif file_type == 'npy':
            np.save(file=file_path, arr=dataset)
