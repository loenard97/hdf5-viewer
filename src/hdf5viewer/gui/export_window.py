import os
import pathlib

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog, QFormLayout, QLabel, QPushButton, \
    QHBoxLayout

from hdf5viewer.img.img_path import img_path
from hdf5viewer.lib_h5.file_export import export_h5file

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hdf5viewer.gui.main_window import MainWindow


class ExportWindow(QWidget):
    """
    Export Item Window
    """
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self._main_window = main_window

        icon_path = str(pathlib.Path(img_path(), "export.svg").absolute())
        self.setWindowTitle("Export Item")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(icon_path))

        self._out_path = ''

        print(f"{main_window.selected_item=}")

        if main_window.selected_item is None:
            QMessageBox.information(
                self, "Nothing selected", "Please select a File, Group or Dataset you want to export.")
            return

        lyt_settings = QFormLayout()
        lyt_settings.addWidget(QLabel(f"{main_window.selected_item}"))
        lyt_settings.addRow(QLabel("Selected File"), QLabel(f"{main_window.selected_item[0]}"))
        lyt_out_path = QHBoxLayout()
        lbl_out_path = QLabel(self._out_path)
        lyt_out_path.addWidget(lbl_out_path)
        btn_out_path = QPushButton("Choose out path")
        btn_out_path.clicked.connect(self._handle_btn_folder)
        lyt_out_path.addWidget(btn_out_path)
        lyt_settings.addRow("Output File Path", lyt_out_path)

        lyt_buttons = QHBoxLayout()
        btn_export = QPushButton("Export")
        btn_export.clicked.connect(self._handle_btn_export)    # NOQA
        lyt_buttons.addWidget(btn_export)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self._handle_btn_cancel)    # NOQA
        lyt_buttons.addWidget(btn_cancel)

        lyt_total = QVBoxLayout()
        lyt_total.addLayout(lyt_settings)
        lyt_total.addLayout(lyt_buttons)

        self.setLayout(lyt_total)

        self.show()

    @pyqtSlot()
    def _handle_btn_export(self):
        export_h5file(in_path=self._main_window.selected_item[0], out_path=str(pathlib.Path(__file__)), file_type="csv")

    @pyqtSlot()
    def _handle_btn_cancel(self):
        self.close()

    @pyqtSlot()
    def _handle_btn_folder(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Dataset", os.path.expanduser('~'), "CSV File (*.csv);;Numpy File (*.npy);;All Files (*.*)")
