"""About Page rendered with html/about_page.html text."""

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
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTextBrowser, QVBoxLayout, QWidget


class AboutPage(QWidget):
    """About Page rendered with html/about_page.html text."""

    def __init__(self) -> None:
        """About Page rendered with html/about_page.html text."""
        super().__init__()
        if getattr(sys, "frozen", False):
            self._file_dir = os.path.dirname(sys.executable)
        else:
            self._file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.setWindowTitle("About Page")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(os.path.join(self._file_dir, "img", "about.svg")))

        with open(os.path.join(self._file_dir, "html", "about_page.html")) as file:
            html = file.read()
        layout = QVBoxLayout()
        text = QTextBrowser(self)
        text.setOpenExternalLinks(True)
        text.setHtml(html)
        layout.addWidget(text)
        self.setLayout(layout)
        self.show()
