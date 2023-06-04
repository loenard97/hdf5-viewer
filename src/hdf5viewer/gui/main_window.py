import os
import h5py
import logging
import numpy as np
import pyqtgraph as pg

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QIcon, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QTableView, QFormLayout, QWidget, QVBoxLayout, \
    QHBoxLayout, QTreeWidget, QTextBrowser, QComboBox

from hdf5viewer.gui.about_page import AboutPage
from hdf5viewer.gui.export_window import ExportWindow
from hdf5viewer.gui.table_model import TableModel, DataTable
from hdf5viewer.img.img_path import img_path
from hdf5viewer.lib_h5.dataset_types import H5DatasetType
from hdf5viewer.lib_h5.file_size import file_size_to_str


class MainWindow(QMainWindow):

    def __init__(self, init_file_path: str):
        super().__init__(flags=Qt.WindowType.Window)
        self.setAcceptDrops(True)

        # Variables
        self._cur_file = ''
        self._cur_obj_path = ''
        self._icon_dir = img_path()

        # Appearance
        self.setMinimumSize(1400, 700)
        self.setWindowTitle("HDF5 Viewer")
        self.setWindowIcon(QIcon(os.path.join(self._icon_dir, "file.svg")))

        # Layout Right Side
        self._tm_dataset = TableModel(header=['Attribute', 'Value'])
        self._tv_dataset = QTableView()
        self._tv_dataset.setModel(self._tm_dataset)
        self._tv_dataset.setColumnWidth(1, 300)
        lyt_plot_type = QFormLayout()
        self._cb_plot_type = QComboBox()
        self._cb_plot_type.addItems(["Auto", "String", "Array1D", "Array2D", "ImageRGB", "Table"])
        self._cb_plot_type.currentTextChanged.connect(self._handle_plot_type_changed)    # NOQA
        lyt_plot_type.addRow("Plot as", self._cb_plot_type)
        self._pw_dataset = pg.PlotWidget()
        self._lyt_dataset = QVBoxLayout()
        self._lyt_dataset.addWidget(self._tv_dataset)
        self._lyt_dataset.addLayout(lyt_plot_type)
        self._lyt_dataset.addWidget(self._pw_dataset)

        # Center Layout
        self._tw_file = QTreeWidget(self)
        self._tw_file.setColumnCount(2)
        self._tw_file.setHeaderLabels(["Name", "Type"])
        self._tw_file.setColumnWidth(0, 500)
        self._tw_file.setAcceptDrops(True)
        self._tw_file.currentItemChanged.connect(self._handle_item_changed)    # NOQA
        wgt_total = QHBoxLayout()
        wgt_total.addWidget(self._tw_file)
        wgt_total.addLayout(self._lyt_dataset)
        wgt_central = QWidget()
        wgt_central.setLayout(wgt_total)
        self.setCentralWidget(wgt_central)

        # File Menu
        mbr_file = self.menuBar().addMenu("&File")
        act_file = QAction('&Open File...', self)
        act_file.setIcon(QIcon(os.path.join(self._icon_dir, "file.svg")))
        act_file.setShortcut('Ctrl+O')
        act_file.triggered.connect(self._handle_action_open_file)    # NOQA
        mbr_file.addAction(act_file)
        act_open_folder = QAction('&Open Folder...', self)
        act_open_folder.setIcon(QIcon(os.path.join(self._icon_dir, "group.svg")))
        act_open_folder.triggered.connect(self._handle_action_open_folder)    # NOQA
        mbr_file.addAction(act_open_folder)
        act_clear_files = QAction('&Clear all Files', self)
        act_clear_files.setIcon(QIcon(os.path.join(self._icon_dir, "file_clear.svg")))
        act_clear_files.triggered.connect(self._handle_action_clear_files)    # NOQA
        mbr_file.addAction(act_clear_files)
        mbr_file.addSeparator()
        act_quit = QAction("&Quit", self)
        act_quit.setIcon(QIcon(os.path.join(self._icon_dir, "quit.svg")))
        act_quit.setShortcut("Ctrl+Q")
        act_quit.triggered.connect(self._handle_close)    # NOQA
        mbr_file.addAction(act_quit)

        # Export Menu
        mbr_export = self.menuBar().addMenu("&Export")
        act_export = QAction('&Export Item...', self)
        act_export.setIcon(QIcon(os.path.join(self._icon_dir, "export.svg")))
        act_export.setShortcut('Ctrl+E')
        act_export.triggered.connect(self._handle_action_export)    # NOQA
        mbr_export.addAction(act_export)

        # Help Menu
        mbr_help = self.menuBar().addMenu("&Help")
        act_about = QAction("&About Page...", self)
        act_about.setIcon(QIcon(os.path.join(self._icon_dir, "about.svg")))
        act_about.triggered.connect(self._handle_action_about)    # NOQA
        mbr_help.addAction(act_about)

        # Open File when double-clicking
        if init_file_path:
            self._open_file(init_file_path)

    @property
    def selected_item(self):
        """
        Tuple of selected file name, object name and object type
        """
        if not self._cur_obj_path:
            obj_type = h5py.File
        else:
            with h5py.File(self._cur_file, 'r') as file:
                obj_type = type(file[self._cur_obj_path])

        return self._cur_file, self._cur_obj_path, obj_type

    def _open_file(self, file_path):
        """
        Open one File
        :param str file_path: File Path
        """
        logging.info(f"Open file '{file_path}'")
        try:
            # Load TreeView from File
            with h5py.File(file_path, 'r') as file:
                parent_item = QTreeWidgetItem()
                parent_item.setText(0, file_path)
                parent_item.setText(1, "HDF5 File")
                parent_item.setIcon(1, QIcon(os.path.join(self._icon_dir, "file.svg")))
                self._hdf5_recursion(hdf5_object=file, root=parent_item, parent=parent_item)
                self._tw_file.insertTopLevelItem(self._tw_file.topLevelItemCount(), parent_item)
        except (OSError, ValueError) as err:
            logging.warning(f"Failed to open file. Error: '{err}'")

    def _tree_recursion(self, item, path):
        """
        Get Array of all Parents
        :param QTreeWidgetItem item:
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
                child_item.setIcon(1, QIcon(os.path.join(self._icon_dir, "group.svg")))
                parent.addChild(child_item)
                self._hdf5_recursion(value, root, child_item)

            elif str(type(value)) == "<class 'h5py._hl.dataset.Dataset'>":
                child_item = QTreeWidgetItem(parent, type=0)
                child_item.setText(0, name)
                child_item.setText(1, "Dataset")
                child_item.setIcon(1, QIcon(os.path.join(self._icon_dir, "dataset.svg")))
                parent.addChild(child_item)

    @pyqtSlot()
    def _plot_data(self, plot_type=None) -> None:
        """
        Update Plot Widget
        :param str plot_type: Plot Type
        """
        # logging.info(f"Plot dataset as '{plot_type}'")
        if self._cur_file is None or not self._cur_obj_path or not os.path.exists(self._cur_file):
            return

        with h5py.File(self._cur_file, 'r') as file:
            data = np.array(file[self._cur_obj_path])

        if plot_type and plot_type != "Auto":
            data_type = H5DatasetType.from_string(plot_type)
        else:
            data_type = H5DatasetType.from_numpy_array(data)

        new_widget: QTextBrowser | pg.PlotWidget | pg.ImageView | QTableView | QWidget
        if data_type == H5DatasetType.String:
            label = "Could not cast to String"
            try:
                label = str(data)
            except (TypeError, AttributeError) as err:
                logging.warning(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
                try:
                    label = '\n'.join([e.decode() for e in data])
                except (TypeError, AttributeError) as err:
                    logging.warning(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
            new_widget = QTextBrowser()
            new_widget.setText(label)
        elif data_type == H5DatasetType.Array1D:
            new_widget = pg.PlotWidget()
            new_widget.plot(data)
        elif data_type == H5DatasetType.Array2D:
            new_widget = pg.ImageView()
            try:
                new_widget.setImage(data)
            except Exception as err:
                logging.warning(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
                return
            new_widget.setColorMap(pg.colormap.get("inferno"))
        elif data_type == H5DatasetType.Table:
            new_widget = QTableView()
            model = DataTable(data)
            new_widget.setModel(model)
        elif data_type == H5DatasetType.ImageRGB:
            data = np.sum(data, axis=0)
            new_widget = pg.ImageView()
            try:
                new_widget.setImage(data)
            except Exception as err:
                logging.warning(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
                return
            new_widget.setColorMap(pg.colormap.get("inferno"))
        else:
            new_widget = QWidget()

        # Replace old Plot Widget
        self._lyt_dataset.replaceWidget(self._pw_dataset, new_widget)
        self._pw_dataset.hide()
        self._pw_dataset.destroy()
        self._pw_dataset = new_widget

    # ----- Drag & Drop ----- #
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

    # ----- Slots ----- #
    @pyqtSlot(str)
    def _handle_plot_type_changed(self, plot_type):
        self._plot_data(plot_type)

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
        self._cur_file = parents_list[0]
        self._cur_obj_path = path

        if len(parents_list) == 1:
            self._tm_dataset.resetData()
            self._tm_dataset.appendRow(["Name", parents_list[0]])
            self._tm_dataset.appendRow(["File Size", file_size_to_str(parents_list[0])])
            return

        with h5py.File(parents_list[0], 'r') as file:
            h5_obj = file[path]

            if str(type(h5_obj)) == "<class 'h5py._hl.group.Group'>":
                self._tm_dataset.resetData()
                self._tm_dataset.appendRow(["Name", str(h5_obj.name)])

            elif str(type(h5_obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                self._tm_dataset.resetData()
                self._tm_dataset.appendRow(["Name", str(h5_obj.name)])
                self._tm_dataset.appendRow(["Size", str(h5_obj.size)])
                self._tm_dataset.appendRow(["Shape", str(h5_obj.shape)])
                self._tm_dataset.appendRow(["Dimensions", str(h5_obj.ndim)])
                self._tm_dataset.appendRow(["Data Type", str(h5_obj.dtype)])

        self._plot_data(self._cb_plot_type.currentText())

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
        self._tw_file.clear()
        self._tm_dataset.resetData()

    @pyqtSlot()
    def _handle_action_export(self):
        """
        Export selected Item
        """
        self._export_window = ExportWindow(main_window=self)

    @pyqtSlot()
    def _handle_action_about(self):
        """
        Open About Page
        """
        self._about_page = AboutPage()

    @pyqtSlot()
    def _handle_close(self):
        """
        Close Window
        """
        self.close()
