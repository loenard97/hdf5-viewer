"""Main Window of the GUI."""

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

import logging
import os
import pathlib
import sys
from typing import Any

import h5py
import numpy as np
import pyqtgraph as pg
from natsort import natsorted
from PyQt6.QtCore import (
    QModelIndex,
    QPoint,
    QSettings,
    QSize,
    QSortFilterProxyModel,
    Qt,
    pyqtSlot,
)
from PyQt6.QtGui import (
    QAction,
    QCloseEvent,
    QDragEnterEvent,
    QDropEvent,
    QIcon,
    QKeySequence,
    QShortcut,
    QStandardItem,
    QStandardItemModel,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableView,
    QTextBrowser,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from src.gui.about_page import AboutPage
from src.gui.export_window import ExportWindow
from src.gui.table_model import DataTable, TableModel
from src.img.img_path import img_path
from src.lib_h5.dataset_types import H5DatasetType
from src.lib_h5.file_size import file_size_to_str


class MainWindow(QMainWindow):
    """Start Main Window of the GUI."""

    def __init__(self) -> None:
        """Start Main Window of the GUI."""
        super().__init__(flags=Qt.WindowType.Window)
        self.setAcceptDrops(True)

        # Variables
        self.cur_file = pathlib.Path()
        self.cur_obj_path = ""
        self.icon_dir = img_path()

        # Appearance
        settings = QSettings()
        self.setMinimumSize(1400, 700)
        self.setWindowTitle("HDF5 Viewer")
        self.resize(settings.value("main_window/size", defaultValue=QSize(1400, 700)))
        self.move(settings.value("main_window/position", defaultValue=QPoint(300, 150)))
        self.setWindowIcon(QIcon(str(pathlib.Path(self.icon_dir, "file.svg"))))

        # Layout Right Side
        self.table_model_dataset = TableModel(header=["Attribute", "Value"])
        self.table_view_dataset = QTableView()
        self.table_view_dataset.setModel(self.table_model_dataset)
        self.table_view_dataset.setColumnWidth(1, 300)
        lyt_plot_type = QFormLayout()
        self.cb_plot_type = QComboBox()
        self.cb_plot_type.addItems(
            ["Auto", "String", "Array1D", "Array2D", "ImageRGB", "Table"]
        )
        self.cb_plot_type.currentTextChanged.connect(  # NOQA
            self._handle_plot_type_changed
        )
        lyt_plot_type.addRow("Plot as", self.cb_plot_type)
        self.plot_wgt_dataset = pg.PlotWidget()
        self.lyt_dataset = QVBoxLayout()
        self.lyt_dataset.addWidget(self.table_view_dataset)
        self.lyt_dataset.addLayout(lyt_plot_type)
        self.lyt_dataset.addWidget(self.plot_wgt_dataset)

        # Center Layout
        self.tree_view_file = QTreeView()
        self.tree_model_file = QStandardItemModel()
        self.tree_model_file.setHorizontalHeaderLabels(["Name", "Type"])
        self.tree_model_file_proxy = QSortFilterProxyModel()
        self.tree_model_file_proxy.setRecursiveFilteringEnabled(True)

        self.tree_model_file_proxy.setSourceModel(self.tree_model_file)
        self.tree_view_file.setModel(self.tree_model_file_proxy)
        self.tree_view_file.setColumnWidth(0, 500)
        self.tree_view_file.setAcceptDrops(True)
        self.tree_view_file.activated.connect(self._handle_item_changed)

        # # self._tw_file.setSelectionMode(QAbstractItemView.selectionMode(self._tw_file).ExtendedSelection)
        # # self._tw_file.setAlternatingRowColors(True)

        self.btn_filter_regex = QPushButton("RegExp")
        self.btn_filter_regex.setCheckable(True)
        self.btn_filter_regex.clicked.connect(self._handle_filter_changed)
        self.btn_filter_case = QPushButton("Cc")
        self.btn_filter_case.setCheckable(True)
        self.btn_filter_case.clicked.connect(self._handle_filter_changed)
        self.le_filter = QLineEdit()
        self.le_filter.setPlaceholderText("Search in all files (press 'f' to focus)")
        self.act_filter = QShortcut(QKeySequence(Qt.Key.Key_F), self)
        self.act_filter.activated.connect(self.le_filter.setFocus)
        self.le_filter.textEdited.connect(self._handle_filter_changed)

        lyt_filter = QHBoxLayout()
        lyt_filter.addWidget(self.btn_filter_regex)
        lyt_filter.addWidget(self.btn_filter_case)
        lyt_filter.addWidget(self.le_filter)

        lyt_file_tree = QVBoxLayout()
        lyt_file_tree.addWidget(self.tree_view_file)
        lyt_file_tree.addLayout(lyt_filter)

        wgt_total = QHBoxLayout()
        wgt_total.addLayout(lyt_file_tree)
        wgt_total.addLayout(self.lyt_dataset)
        wgt_central = QWidget()
        wgt_central.setLayout(wgt_total)
        self.setCentralWidget(wgt_central)

        # File Menu
        if (menu_bar := self.menuBar()) is None:
            return
        if (mbr_file := menu_bar.addMenu("&File")) is not None:
            act_file = QAction("&Open File...", self)
            act_file.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "file.svg"))))
            act_file.setShortcut("Ctrl+O")
            act_file.triggered.connect(self._handle_action_open_file)  # NOQA
            mbr_file.addAction(act_file)
            act_open_folder = QAction("&Open Folder...", self)
            act_open_folder.setIcon(
                QIcon(str(pathlib.Path(self.icon_dir, "group.svg")))
            )
            act_open_folder.triggered.connect(self._handle_action_open_folder)  # NOQA
            mbr_file.addAction(act_open_folder)
            act_clear_files = QAction("&Clear all Files", self)
            act_clear_files.setIcon(
                QIcon(str(pathlib.Path(self.icon_dir, "file_clear.svg")))
            )
            act_clear_files.triggered.connect(self._handle_action_clear_files)  # NOQA
            mbr_file.addAction(act_clear_files)
            mbr_file.addSeparator()
            act_quit = QAction("&Quit", self)
            act_quit.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "quit.svg"))))
            act_quit.setShortcut("Ctrl+Q")
            act_quit.triggered.connect(self._handle_close)  # NOQA
            mbr_file.addAction(act_quit)

        # Export Menu
        if (mbr_export := menu_bar.addMenu("&Export")) is not None:
            act_export = QAction("&Export Item...", self)
            act_export.setIcon(QIcon(os.path.join(self.icon_dir, "export.svg")))
            act_export.setShortcut("Ctrl+E")
            act_export.triggered.connect(self._handle_action_export)  # NOQA
            mbr_export.addAction(act_export)

        # Help Menu
        if (mbr_help := menu_bar.addMenu("&Help")) is not None:
            act_about = QAction("&About Page...", self)
            act_about.setIcon(QIcon(os.path.join(self.icon_dir, "about.svg")))
            act_about.triggered.connect(self._handle_action_about)  # NOQA
            mbr_help.addAction(act_about)

        # Open File when double-clicking
        if len(sys.argv) > 1:
            self._open_file(pathlib.Path(sys.argv[0]))
        for file in settings.value("settings/last_opened_files", ()):
            self._open_file(file)

    @property
    def selected_item(self) -> tuple[pathlib.Path, str, Any]:
        """Tuple of selected file name, object name and object type."""
        if not self.cur_obj_path:
            obj_type = h5py.File
        else:
            with h5py.File(self.cur_file, "r") as file:
                obj_type = type(file[self.cur_obj_path])

        return self.cur_file, self.cur_obj_path, obj_type

    @property
    def opened_files(self) -> tuple[pathlib.Path, ...]:
        """Currently opened files."""
        file_paths = []
        for i in range(self.tree_model_file.rowCount()):
            if (item := self.tree_model_file.item(i, 0)) is not None:
                file_paths.append(pathlib.Path(item.text()))
        return tuple(file_paths)

    def _open_file(self, file_path: pathlib.Path) -> None:
        """
        Open one File.

        :param str file_path: File Path
        """
        logging.info(f"Open file '{file_path}'")
        try:
            # Load TreeModel from File
            with h5py.File(file_path, "r") as file:
                parent_name = QStandardItem(str(file_path))
                parent_name.setEditable(False)
                parent_text = QStandardItem("HDF5 File")
                parent_text.setEditable(False)
                parent_text.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "file.svg"))))
                self._hdf5_recursion(
                    hdf5_object=file, root=parent_name, parent=parent_name
                )
                self.tree_model_file.appendRow([parent_name, parent_text])
        except (OSError, ValueError) as err:
            logging.warning(f"Failed to open file. Error: '{err}'")

    def _hdf5_recursion(
        self,
        hdf5_object: h5py.File | h5py.Group | h5py.Dataset,
        root: QStandardItem,
        parent: QStandardItem,
    ) -> None:
        """Recursively go through hdf5 File and construct tree view model."""
        for name in natsorted(hdf5_object):
            value = hdf5_object[name]
            if isinstance(value, h5py.Group):
                child_name = QStandardItem(name)
                child_name.setEditable(False)
                child_type = QStandardItem("Group")
                child_type.setEditable(False)
                child_type.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "group.svg"))))
                parent.appendRow([child_name, child_type])
                self._hdf5_recursion(value, root, child_name)
            elif isinstance(value, h5py.Dataset):
                child_name = QStandardItem(name)
                child_name.setEditable(False)
                child_type = QStandardItem("Dataset")
                child_type.setEditable(False)
                child_type.setIcon(
                    QIcon(str(pathlib.Path(self.icon_dir, "dataset.svg")))
                )
                parent.appendRow([child_name, child_type])

    @pyqtSlot()
    def _plot_data(self, plot_type: str = "") -> None:
        """
        Update Plot Widget.

        :param str plot_type: Plot Type
        """
        logging.debug(f"Plot dataset as '{plot_type}'")
        if (
            self.cur_file is None
            or not self.cur_obj_path
            or not os.path.exists(self.cur_file)
        ):
            return

        with h5py.File(self.cur_file, "r") as file:
            data = np.array(file[self.cur_obj_path])

        if plot_type and plot_type != "Auto":
            data_type = H5DatasetType.from_string(plot_type)
        else:
            data_type = H5DatasetType.from_numpy_array(data)

        new_widget: QTextBrowser | pg.PlotWidget | pg.ImageView | QTableView | QWidget
        if data_type == H5DatasetType.String:
            if data.ndim == 0:
                label = data.item()
                if isinstance(label, bytes):
                    label = label.decode()
                label = str(label)
            else:
                label = str(data)
            new_widget = QTextBrowser()
            new_widget.setText(label)
        elif data_type == H5DatasetType.Array1D:
            new_widget = pg.PlotWidget()
            try:
                new_widget.plot(data)
            except Exception as err:
                logging.error(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
                return
        elif data_type == H5DatasetType.Array2D:
            new_widget = pg.ImageView()
            try:
                new_widget.setImage(data)
            except Exception as err:
                logging.error(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
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
                logging.error(f"Failed plot dataset as '{plot_type}'. Error: '{err}'")
                return
            new_widget.setColorMap(pg.colormap.get("inferno"))
        else:
            new_widget = QWidget()

        # Replace old Plot Widget
        self.lyt_dataset.replaceWidget(self.plot_wgt_dataset, new_widget)
        self.plot_wgt_dataset.hide()
        self.plot_wgt_dataset.destroy()
        self.plot_wgt_dataset = new_widget

    # ----- Drag & Drop ----- #
    def dragEnterEvent(self, event: QDragEnterEvent | None) -> None:
        """Accept Drag Events for h5 and hdf5 files to initiate Drag & Drop Events."""
        if event is None:
            return
        if (mime_data := event.mimeData()) is None:
            return
        for file in mime_data.text().split("\n"):
            if len(file) == 0:
                continue
            if not file.split(".")[-1] in ["h5", "hdf5"]:
                return
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent | None) -> None:
        """Open Files that are dropped into Window."""
        if event is None:
            return
        if (mime_data := event.mimeData()) is None:
            return
        for file in mime_data.text().split("\n"):
            file = file.removeprefix("file:")
            self._open_file(pathlib.Path(file))
        event.acceptProposedAction()

    # ----- Slots ----- #
    @pyqtSlot(str)
    def _handle_plot_type_changed(self, plot_type: str) -> None:
        """Update plot when new plot type is selected."""
        self._plot_data(plot_type)

    @pyqtSlot(QModelIndex)
    def _handle_item_changed(self, index: None | QModelIndex) -> None:
        """Update Info of currently selected Item."""
        if index is None:
            return

        parents_list = [index.data()]
        self._tree_recursion(index, parents_list)
        parents_list.reverse()
        path = ""
        for e in parents_list[1:]:
            path += "/" + e
        self.cur_file = pathlib.Path(parents_list[0])
        self.cur_obj_path = path

        if len(parents_list) == 1:
            self.table_model_dataset.resetData()
            self.table_model_dataset.appendRow(["Name", parents_list[0]])
            self.table_model_dataset.appendRow(
                ["File Size", file_size_to_str(parents_list[0])]
            )
            return

        with h5py.File(parents_list[0], "r") as file:
            h5_obj = file[path]

            if isinstance(h5_obj, h5py.Group):
                self.table_model_dataset.resetData()
                self.table_model_dataset.appendRow(["Name", str(h5_obj.name)])

            elif isinstance(h5_obj, h5py.Dataset):
                self.table_model_dataset.resetData()
                self.table_model_dataset.appendRow(["Name", str(h5_obj.name)])
                self.table_model_dataset.appendRow(
                    ["Data", f"shape {h5_obj.shape} of type {h5_obj.dtype}"]
                )

                for attribute, value in h5_obj.attrs.items():
                    self.table_model_dataset.appendRow([attribute, str(value)])

        self._plot_data(self.cb_plot_type.currentText())

    def _tree_recursion(self, item: QModelIndex, path: list[str]) -> None:
        """Get Array of all Parents."""
        if (data := item.parent().data()) is None:
            return
        path.append(data)
        self._tree_recursion(item.parent(), path)

    @pyqtSlot()
    def _handle_filter_changed(self) -> None:
        text = self.le_filter.text()
        if text:
            self.tree_view_file.expandAll()
        else:
            self.tree_view_file.collapseAll()
        self.tree_model_file_proxy.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseSensitive
            if self.btn_filter_case.isChecked()
            else Qt.CaseSensitivity.CaseInsensitive
        )
        if self.btn_filter_regex.isChecked():
            self.tree_model_file_proxy.setFilterRegularExpression(text)
        else:
            self.tree_model_file_proxy.setFilterFixedString(text)

    @pyqtSlot()
    def _handle_action_open_file(self) -> None:
        """Open HDF5 Files."""
        settings = QSettings()
        folder: pathlib.Path = pathlib.Path(
            settings.value(
                "paths/last_opened_file_directory", defaultValue=os.path.expanduser("~")
            )
        )
        default_path = (
            str(folder.absolute())
            if folder.absolute().exists()
            else os.path.expanduser("~")
        )
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            default_path,
            "HDF5 File (*.hdf5, *.h5);;All Files (*.*)",
        )
        if not file_paths:
            return

        settings.setValue(
            "paths/last_opened_file_directory", pathlib.Path(file_paths[0]).parent
        )
        for file in file_paths:
            self._open_file(pathlib.Path(file))

    @pyqtSlot()
    def _handle_action_open_folder(self) -> None:
        """Open all HDF5 Files in a Folder."""
        settings = QSettings()
        folder: pathlib.Path = settings.value(
            "paths/last_opened_folder_directory",
            defaultValue=pathlib.Path(os.path.expanduser("~")),
        )
        default_path = (
            str(folder.absolute())
            if folder.absolute().exists()
            else os.path.expanduser("~")
        )
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", default_path
        )
        if not folder_path:
            return

        settings.setValue(
            "paths/last_opened_folder_directory", pathlib.Path(folder_path)
        )
        for file in os.listdir(folder_path):
            self._open_file(pathlib.Path(folder_path, file))

    @pyqtSlot()
    def _handle_action_clear_files(self) -> None:
        """Clear Tree Widget."""
        self.tree_model_file.clear()
        self.table_model_dataset.resetData()

    @pyqtSlot()
    def _handle_action_export(self) -> None:
        """Export selected Item."""
        self._export_window = ExportWindow(main_window=self)

    @pyqtSlot()
    def _handle_action_about(self) -> None:
        """Open About Page."""
        self._about_page = AboutPage()

    @pyqtSlot()
    def _handle_close(self) -> None:
        """Close Window."""
        self.close()

    @pyqtSlot()
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """Close Window."""
        if a0 is None:
            return

        settings = QSettings()
        settings.setValue("main_window/size", self.size())
        settings.setValue("main_window/position", self.pos())
        settings.setValue("settings/last_opened_files", self.opened_files)
        settings.sync()
