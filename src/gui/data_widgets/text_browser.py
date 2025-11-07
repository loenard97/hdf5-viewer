import os

from natsort import natsorted
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QTextBrowser


class DataTextBrowser(QTextBrowser):

    def __init__(self, data):
        super().__init__()
        if data.ndim == 0:
            label = data.item()
            if isinstance(label, bytes):
                label = label.decode()
            label = str(label)
        else:
            label = str(data)
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)


class FileTextBrowser(QTextBrowser):

    def __init__(self, data):
        super().__init__()
        label = "HDF5 File (" + self.file_size_to_str(str(data)) + "):\n" + str(data)
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)

    @staticmethod
    def file_size_to_str(file_path: str) -> str:
        """Get formatted file size."""
        size = os.path.getsize(file_path)

        if size > 1024**3:
            return f"{size / 1024 ** 3:.2f} GB"
        elif size > 1024**2:
            return f"{size / 1024 ** 2:.2f} MB"
        elif size > 1024:
            return f"{size / 1024:.2f} kB"
        else:
            return f"{size} bytes"


class GroupTextBrowser(QTextBrowser):

    def __init__(self, data):
        super().__init__()
        label = "Group:\n"
        for e in natsorted(data):
            label += " - " + str(e) + "\n"
        font_id = QFontDatabase.addApplicationFont("fonts/NotoSansMono/NotoSansMono-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[-1], 10)
        self.setFont(font)
        self.setText(label)
