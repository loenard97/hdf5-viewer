import sys

from PyQt6.QtWidgets import QApplication

from src.main_window import MainWindow

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'hdf5viewer')


def main():
    if len(sys.argv) >= 2:
        open_file = sys.argv[1]
    else:
        open_file = None

    app = QApplication(sys.argv)
    main_win = MainWindow(open_file)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
