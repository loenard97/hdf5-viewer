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
import pathlib
import sys
from collections.abc import Generator
from typing import override

import h5py
from natsort import natsorted
from PyQt6.QtCore import QModelIndex, QPoint, QSettings, QSize, Qt, pyqtSlot
from PyQt6.QtGui import (
    QAction,
    QCloseEvent,
    QDragEnterEvent,
    QDropEvent,
    QIcon,
    QStandardItem,
)
from PyQt6.QtWidgets import (
    QCompleter,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QVBoxLayout,
    QWidget,
)

from src.gui.data_widgets.factory import DataWidgetFactory
from src.gui.main_window.left_side_layout import MainWindowLayoutLeftSide
from src.gui.main_window.right_side_layout import MainWindowLayoutRightSide
from src.icons.icons_path import icons_path


class MainWindow(QMainWindow):
    """Start Main Window of the GUI."""

    def __init__(self) -> None:
        """Start Main Window of the GUI."""
        super().__init__(flags=Qt.WindowType.Window)

        self.cur_file = pathlib.Path()
        self.cur_obj_path = ""
        self.icons_path = icons_path()

        settings = QSettings()
        self.setAcceptDrops(True)
        self.setMinimumSize(1400, 700)
        self.setWindowTitle("HDF5 Viewer")
        self.resize(settings.value("main_window/size", defaultValue=QSize(1400, 700)))
        self.move(settings.value("main_window/position", defaultValue=QPoint(300, 150)))
        self.setWindowIcon(QIcon(str(pathlib.Path(self.icons_path, "file.svg"))))

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        self.left_layout = MainWindowLayoutLeftSide(main_window=self)
        layout.addLayout(self.left_layout)
        self.right_layout = MainWindowLayoutRightSide(main_window=self)
        layout.addLayout(self.right_layout)

        layout_central_widget = QVBoxLayout()
        layout_central_widget.setContentsMargins(0, 0, 0, 0)
        layout_central_widget.addLayout(layout)
        layout_central_widget.setAlignment(Qt.AlignmentFlag.AlignTop)

        widget_central = QWidget()
        widget_central.setLayout(layout_central_widget)
        self.setCentralWidget(widget_central)

    @staticmethod
    def iter_items(root: QStandardItem) -> Generator[object, object, object]:
        """Iterate recursively through all children of a QStandardItem."""

        def recurse(parent: QStandardItem) -> Generator[object, object, object]:
            for row in range(parent.rowCount()):
                if (child := parent.child(row, 0)) is not None:
                    yield child.text()
                    if child.hasChildren():
                        yield from recurse(child)

            return None

        if root is not None:
            yield from recurse(root)

        return None

    @property
    def selected_item(self) -> tuple[pathlib.Path, str, object]:
        """Tuple of selected file name, object name and object type."""
        obj_type = None
        if not self.cur_obj_path:
            obj_type = h5py.File
        else:
            with h5py.File(self.cur_file, "r") as file:
                obj_type = type(file[self.cur_obj_path])

        return self.cur_file, self.cur_obj_path, obj_type

    @property
    def opened_file(self) -> pathlib.Path:
        """Currently opened file."""
        item = self.left_layout.tree_model_file.item(0, 0)

        return pathlib.Path(item.text())

    def open_file(self, file_path: pathlib.Path) -> None:
        """
        Open one File.

        :param str file_path: File Path
        """
        self.handle_action_clear_files()
        logger = logging.getLogger(__name__)
        logger.info("Open file '%s'", file_path)
        try:
            # Load TreeModel from File
            with h5py.File(file_path, "r") as file:
                parent_name = QStandardItem(str(file_path))
                parent_name.setEditable(False)
                parent_text = QStandardItem("HDF5 File")
                parent_text.setEditable(False)
                parent_text.setIcon(QIcon(str(pathlib.Path(self.icons_path, "file.svg"))))
                self.hdf5_recursion(hdf5_object=file, root=parent_name, parent=parent_name)
                self.left_layout.tree_model_file.appendRow([parent_name, parent_text])
        except (OSError, ValueError):
            logger = logging.getLogger(__name__)
            logger.exception("Failed to open file. Error: '%s'")

        if (root := self.left_layout.tree_model_file.invisibleRootItem()) is not None:
            self.left_layout.completer = QCompleter(list(self.iter_items(root)))
            self.left_layout.completer.setCaseSensitivity(
                Qt.CaseSensitivity.CaseSensitive
                if self.left_layout.btn_filter_case.isChecked()
                else Qt.CaseSensitivity.CaseInsensitive,
            )
            self.left_layout.le_filter.setCompleter(self.left_layout.completer)

        self.left_layout.tree_view_file.setColumnWidth(0, 500)

    # def stack_impl(self):
    #     path = pathlib.Path(
    #         r"D:\Documents\Uni Daten\2025-06-17_lia-deviation\2025-09-24_11-34-31_cwodmrlia\raw_data.h5")
    #
    #     with h5py.File(path, "r") as file:
    #         stack: list[str] = []
    #         stack.extend(file)
    #         stack_pos = 0
    #         stack_len = len(stack)
    #
    #         while stack_pos < stack_len:
    #             if isinstance(file[stack[stack_pos]], h5py.Group):
    #                 for h5_object in natsorted(file[stack[stack_pos]]):
    #                     stack.append(stack[stack_pos] + "/" + h5_object)
    #                 stack.pop(stack_pos)
    #                 continue
    #
    #             if isinstance(file[stack[stack_pos]], h5py.Dataset):
    #                 stack_len = len(stack)
    #                 stack_pos += 1
    #                 continue
    #
    #             raise ValueError
    #
    #     return stack

    def hdf5_recursion(
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
                child_type.setIcon(QIcon(str(pathlib.Path(self.icons_path, "group.svg"))))
                parent.appendRow([child_name, child_type])
                self.hdf5_recursion(value, root, child_name)
            elif isinstance(value, h5py.Dataset):
                child_name = QStandardItem(name)
                child_name.setEditable(False)
                child_type = QStandardItem("Dataset")
                child_type.setEditable(False)
                child_type.setIcon(QIcon(str(pathlib.Path(self.icons_path, "dataset.svg"))))
                parent.appendRow([child_name, child_type])

    @pyqtSlot()
    def plot_data(self, plot_type: str = "") -> None:
        """
        Update Plot Widget.

        :param str plot_type: Plot Type
        """
        if self.cur_file is None or not pathlib.Path(self.cur_file).exists():
            return

        # create new data widget depending on what type of data to show
        new_widget = DataWidgetFactory.get_data_widget_from_data(self.cur_file, self.cur_obj_path, plot_type)

        # replace old data widget
        self.right_layout.replaceWidget(self.right_layout.plot_wgt_dataset, new_widget)
        self.right_layout.plot_wgt_dataset.hide()
        self.right_layout.plot_wgt_dataset.destroy()
        self.right_layout.plot_wgt_dataset = new_widget

    # ----- Drag & Drop ----- #
    @override
    def dragEnterEvent(self, event: QDragEnterEvent | None) -> None:
        """Accept Drag Events for h5 and hdf5 files to initiate Drag & Drop Events."""
        if event is None:
            return
        for file in event.mimeData().text().split("\n"):
            if len(file) == 0:
                continue
            if file.split(".")[-1] not in ["h5", "hdf5"]:
                return
        event.acceptProposedAction()

    @override
    def dropEvent(self, event: QDropEvent | None) -> None:
        """Open Files that are dropped into Window."""
        if event is None:
            return
        for file in event.mimeData().text().split("\n"):
            if sys.platform == "win32":
                self.open_file(pathlib.Path(file[8:]))
            else:
                self.open_file(pathlib.Path(file.removeprefix("file:")))
        event.acceptProposedAction()

    # ----- Slots ----- #
    @pyqtSlot(str)
    def handle_plot_type_changed(self, plot_type: str) -> None:
        """Update plot when new plot type is selected."""
        self.plot_data(plot_type)

    @pyqtSlot(QModelIndex)
    def handle_item_changed(self, index: None | QModelIndex) -> None:
        """Update Info of currently selected Item."""
        if index is None:
            return

        parents_list = [index.data()]
        self.tree_recursion(index, parents_list)
        parents_list.reverse()
        path = ""
        for e in parents_list[1:]:
            path += "/" + e
        self.cur_file = pathlib.Path(parents_list[0])
        self.cur_obj_path = path

        self.plot_data(self.right_layout.cb_plot_type.currentText())

    def tree_recursion(self, item: QModelIndex, path: list[str]) -> None:
        """Get Array of all Parents."""
        if (data := item.parent().data()) is None:
            return
        path.append(data)
        self.tree_recursion(item.parent(), path)

    @pyqtSlot()
    def handle_filter_changed(self) -> None:
        """Handle filter changed."""
        text = self.left_layout.le_filter.text()
        if text:
            self.left_layout.tree_view_file.expandAll()
        else:
            self.left_layout.tree_view_file.collapseAll()
        self.left_layout.tree_model_file_proxy.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseSensitive
            if self.left_layout.btn_filter_case.isChecked()
            else Qt.CaseSensitivity.CaseInsensitive,
        )
        if self.left_layout.btn_filter_regex.isChecked():
            self.left_layout.tree_model_file_proxy.setFilterRegularExpression(text)
        else:
            self.left_layout.tree_model_file_proxy.setFilterFixedString(text)
        self.left_layout.completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseSensitive
            if self.left_layout.btn_filter_case.isChecked()
            else Qt.CaseSensitivity.CaseInsensitive,
        )

    @pyqtSlot(QPoint)
    def handle_tree_menu(self, pos: QPoint) -> None:
        """Handle tree menu."""
        menu = QMenu(self)
        index = self.left_layout.tree_view_file.indexAt(pos)
        if index.parent().data() is None:
            action = QAction("Close file", self)
            menu.addAction(action)
            action.triggered.connect(lambda: self.left_layout.tree_model_file.removeRow(index.row()))

        if (viewport := self.left_layout.tree_view_file.viewport()) is not None:
            menu.popup(viewport.mapToGlobal(pos))

    @pyqtSlot()
    def handle_action_open_file(self) -> None:
        """Open HDF5 Files."""
        settings = QSettings()
        try:
            folder: pathlib.Path = pathlib.Path(
                settings.value("paths/last_opened_file_directory", defaultValue=pathlib.Path("~").expanduser()),
            )
            default_path = str(folder.absolute()) if folder.absolute().exists() else str(pathlib.Path("~").expanduser())
        except TypeError:
            default_path = str(pathlib.Path("~").expanduser())
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            default_path,
            "HDF5 File (*.hdf5, *.h5);;All Files (*.*)",
        )
        if not file_paths:
            return

        settings.setValue("paths/last_opened_file_directory", pathlib.Path(file_paths[0]).parent)
        for file in file_paths:
            self.open_file(pathlib.Path(file))

    @pyqtSlot()
    def handle_action_open_folder(self) -> None:
        """Open all HDF5 Files in a Folder."""
        settings = QSettings()
        folder: pathlib.Path = settings.value(
            "paths/last_opened_folder_directory",
            defaultValue=pathlib.Path("~").expanduser(),
        )
        default_path = str(folder.absolute()) if folder.absolute().exists() else str(pathlib.Path("~").expanduser())
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", default_path)
        if not folder_path:
            return

        settings.setValue("paths/last_opened_folder_directory", pathlib.Path(folder_path))
        for file in pathlib.Path(folder_path).iterdir():
            self.open_file(pathlib.Path(folder_path, file))

    @pyqtSlot()
    def handle_action_clear_files(self) -> None:
        """Clear Tree Widget."""
        self.left_layout.tree_model_file.clear()

    @pyqtSlot()
    def handle_close(self) -> None:
        """Close Window."""
        self.close()

    @override
    @pyqtSlot()
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """Close Window."""
        if a0 is None:
            return

        settings = QSettings()
        settings.setValue("main_window/size", self.size())
        settings.setValue("main_window/position", self.pos())
        settings.setValue("settings/last_opened_files", self.opened_file)
        settings.sync()
