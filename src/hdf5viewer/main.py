import sys
import argparse

from PyQt6.QtWidgets import QApplication

from hdf5viewer.cli.parse_cli_args import parse_cli_args
from hdf5viewer.gui.main_window import MainWindow

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'hdf5viewer')


def main():
    parser = argparse.ArgumentParser(
        prog="HDF5 File Viewer",
        description="A File Viewer for HDF5 Files.",
    )
    parser.add_argument("filename", help="H5 file to load", nargs='?', default='')
    parser.add_argument("-e", "--export", help="Export H5 File to output file")
    parser.add_argument("-l", "--list", help="List all Groups and Datasets", action="store_true")
    parser.add_argument("-t", "--tree", help="List all Groups and Datasets recursively as tree", action="store_true")
    parser.add_argument("-p", "--plain", help="Disable pretty printing", action="store_true")
    args = parser.parse_args()

    if args.export is not None or any([args.list, args.tree]):
        parse_cli_args(args)
    else:
        app = QApplication(sys.argv)
        main_win = MainWindow(init_file_path=args.filename)
        main_win.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
