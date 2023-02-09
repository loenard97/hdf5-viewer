import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser


class AboutPage(QWidget):
    """
    About Page render with html/about_page.html text
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Page")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(os.path.join("img", "about.svg")))

        with open(os.path.join("html", "about_page.html")) as file:
            html = file.read()
        layout = QVBoxLayout()
        text = QTextBrowser(self)
        text.setOpenExternalLinks(True)
        text.setHtml(html)
        layout.addWidget(text)
        self.setLayout(layout)
        self.show()
