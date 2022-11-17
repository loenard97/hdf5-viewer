from PyQt6.QtWidgets import QTreeWidget


class FileTreeWidget(QTreeWidget):

    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window

    def dropEvent(self, event):
        # TODO: isn't called for some reason?
        print(event)

    def dragEnterEvent(self, event):
        """
        Open File in MainWindow on DragEvent
        """
        files = event.mimeData().text().split('\n')
        for f in files:
            self._main_window.open_file(f[8:])
