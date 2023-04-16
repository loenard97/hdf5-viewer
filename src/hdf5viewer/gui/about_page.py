import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser


class AboutPage(QWidget):
    """
    About Page rendered with html/about_page.html text
    """
    def __init__(self):
        super().__init__()
        if getattr(sys, 'frozen', False):
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
