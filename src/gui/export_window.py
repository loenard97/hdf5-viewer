"""Export Item Window."""

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

import os
import pathlib
from typing import TYPE_CHECKING

import h5py
from PyQt6.QtCore import QSettings, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.img.img_path import img_path
from src.lib_h5.file_export import export_dataset, export_file, export_group

if TYPE_CHECKING:
    from gui.main_window import MainWindow


class ExportWindow(QWidget):
    """Export Item Window."""

    def __init__(self, main_window: "MainWindow"):
        """Export Item Window."""
        super().__init__()
        self._main_window = main_window

        icon_path = str(pathlib.Path(img_path(), "export.svg").absolute())
        self.setWindowTitle("Export Item")
        # self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(icon_path))

        settings = QSettings()
        self._out_path = settings.value("export_path", "")

        lyt_settings = QFormLayout()
        lyt_settings.addRow(
            QLabel("Selected File"), QLabel(f"{main_window.selected_item[0]}")
        )
        lyt_settings.addRow(
            QLabel("Selected Item"), QLabel(f"{main_window.selected_item[1]}")
        )
        self._cb_file_type = QComboBox()
        self._cb_file_type.addItems(["csv", "npy"])
        lyt_settings.addRow(QLabel("File Type"), self._cb_file_type)

        lyt_buttons = QHBoxLayout()
        btn_export = QPushButton("Export")
        btn_export.clicked.connect(self._handle_btn_export)  # NOQA
        lyt_buttons.addWidget(btn_export)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self._handle_btn_cancel)  # NOQA
        lyt_buttons.addWidget(btn_cancel)

        lyt_total = QVBoxLayout()
        lyt_total.addLayout(lyt_settings)
        lyt_total.addLayout(lyt_buttons)

        self.setLayout(lyt_total)

        self.show()

    @pyqtSlot()
    def _handle_btn_export(self) -> None:
        """Export item."""
        h5file_path, h5obj_path, h5obj_type = self._main_window.selected_item

        if h5obj_type == h5py.Dataset:
            self._out_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Dataset",
                os.path.expanduser("~"),
                "CSV File (*.csv);;Numpy File (*.npy);;All Files (*.*)",
            )
        else:
            self._out_path = QFileDialog.getExistingDirectory(
                self, "Export Group", os.path.expanduser("~")
            )

        settings = QSettings()
        settings.setValue("export_path", self._out_path)

        if os.path.exists(self._out_path):
            if (
                QMessageBox.question(
                    self,
                    "Overwrite",
                    f"The path {self._out_path} already exists. Do you want to overwrite existing files?",
                    buttons=QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.Cancel,
                )
                == QMessageBox.StandardButton.Cancel
            ):
                return

        if h5obj_type == h5py.File:
            export_file(
                input_file=h5file_path,
                output_file=pathlib.Path(self._out_path),
                save_as_type=self._cb_file_type.currentText(),
            )
        elif h5obj_type == h5py.Group:
            export_group(
                input_file=h5file_path,
                group=h5obj_path,
                output_file=pathlib.Path(self._out_path),
                save_as_type=self._cb_file_type.currentText(),
            )
        else:
            export_dataset(
                input_file=h5file_path,
                dataset=h5obj_path,
                output_file=pathlib.Path(self._out_path),
                save_as_type=self._cb_file_type.currentText(),
            )

        self.close()

    @pyqtSlot()
    def _handle_btn_cancel(self) -> None:
        """Close window."""
        self.close()
