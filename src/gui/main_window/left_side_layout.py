"""Layout of the left side of MainWindow of the GUI."""

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

from typing import TYPE_CHECKING

from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QStandardItemModel
from PyQt6.QtWidgets import QCompleter, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QTreeView, QVBoxLayout

if TYPE_CHECKING:
    from src.gui.main_window.main_window import MainWindow


class MainWindowLayoutLeftSide(QVBoxLayout):
    """MainWindow left side layout."""

    def __init__(self, main_window: "MainWindow") -> None:
        """Initialize MainWindow left side layout."""
        super().__init__()

        self.tree_view_file = QTreeView()
        self.tree_view_file.setHeaderHidden(True)
        self.tree_view_file.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view_file.customContextMenuRequested.connect(main_window.handle_tree_menu)
        self.tree_model_file = QStandardItemModel()
        self.tree_model_file.setHorizontalHeaderLabels(["Name", "Type"])
        self.tree_model_file_proxy = QSortFilterProxyModel()
        self.tree_model_file_proxy.setRecursiveFilteringEnabled(True)
        self.tree_model_file_proxy.setSourceModel(self.tree_model_file)
        self.tree_view_file.setModel(self.tree_model_file_proxy)
        # tree.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tree_view_file.setColumnWidth(0, 1500)
        self.tree_view_file.setAcceptDrops(True)
        self.tree_view_file.clicked.connect(main_window.handle_item_changed)

        self.btn_filter_regex = QPushButton("RegExp")
        self.btn_filter_regex.setCheckable(True)
        self.btn_filter_regex.clicked.connect(main_window.handle_filter_changed)
        self.btn_filter_case = QPushButton("Cc")
        self.btn_filter_case.setCheckable(True)
        self.btn_filter_case.clicked.connect(main_window.handle_filter_changed)
        self.le_filter = QLineEdit()
        self.le_filter.setPlaceholderText("Search in all files (press 'f' to focus)")
        self.act_filter = QShortcut(QKeySequence(Qt.Key.Key_F), self)
        self.act_filter.activated.connect(self.le_filter.setFocus)
        self.le_filter.textEdited.connect(main_window.handle_filter_changed)
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.le_filter.setCompleter(self.completer)

        lyt_plot_type = QFormLayout()
        # lyt_plot_type.addRow("Plot as", self.cb_plot_type)

        lyt_filter = QHBoxLayout()
        # lyt_filter.addWidget(self.btn_filter_regex)
        # lyt_filter.addWidget(self.btn_filter_case)
        # lyt_filter.addWidget(self.le_filter)
        btn_open_file = QPushButton("Open File...")
        btn_open_file.clicked.connect(main_window.handle_action_open_file)
        lyt_filter.addWidget(btn_open_file)

        self.addLayout(lyt_filter)
        self.addWidget(self.tree_view_file)
        self.addLayout(lyt_plot_type)
