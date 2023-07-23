"""Settings Window."""

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

import pathlib
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSettings, Qt, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCheckBox, QFormLayout, QLabel, QWidget

from hdf5viewer.img.img_path import img_path

if TYPE_CHECKING:
    from hdf5viewer.gui.main_window import MainWindow


class SettingsWindow(QWidget):
    """Settings Window."""

    def __init__(self, main_window: "MainWindow"):
        """Open settings window."""
        super().__init__()
        self._main_window = main_window

        icon_path = str(pathlib.Path(img_path(), "settings.svg").absolute())
        self.setWindowTitle("Settings")
        # self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(icon_path))

        settings = QSettings()

        # Layout
        lyt_settings = QFormLayout()
        lyt_settings.addRow(QLabel("<b>Settings</b>"))
        self._cb_reopen_files_on_startup = QCheckBox()
        self._cb_reopen_files_on_startup.setCheckState(
            settings.value(
                "settings/reopen_files_on_startup", defaultValue=Qt.CheckState.Unchecked
            )
        )
        self._cb_reopen_files_on_startup.stateChanged.connect(  # NOQA
            self._handle_cb_reopen_files_on_startup
        )
        lyt_settings.addRow(
            QLabel("Reopen last files on startup"), self._cb_reopen_files_on_startup
        )

        self.setLayout(lyt_settings)

        self.show()

    @pyqtSlot(int)
    def _handle_cb_reopen_files_on_startup(self, state: int) -> None:
        """Handle check box reopen files on startup."""
        if state == 0:
            check_state = Qt.CheckState.Unchecked
        elif state == 1:
            check_state = Qt.CheckState.PartiallyChecked
        else:
            check_state = Qt.CheckState.Checked
        settings = QSettings()
        settings.setValue("settings/reopen_files_on_startup", check_state)
