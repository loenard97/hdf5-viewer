"""HDF5 File Viewer entry point."""

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

import argparse
import logging
import os
import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from hdf5viewer.cli.parse_cli_args import parse_cli_args
from hdf5viewer.gui.main_window import MainWindow

if sys.platform == "win32":
    # Set Windows Taskbar Icon
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("hdf5viewer")


def main() -> None:
    """HDF5 File Viewer entry point."""
    parser = argparse.ArgumentParser(
        prog="HDF5 File Viewer",
        description="A File Viewer for HDF5 Files.",
        epilog="HDF5 File Viewer  Copyright (C) 2023  Dennis Lönard\n"
        "This program comes with ABSOLUTELY NO WARRANTY.\n"
        "This is free software, and you are welcome to redistribute it\n"
        "under certain conditions; see the included LICENSE file for details.\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("filename", help="H5 file to load", nargs="?", default="")
    parser.add_argument("-e", "--export", help="Export H5 File to output file")
    parser.add_argument(
        "-l", "--list", help="List all Groups and Datasets", action="store_true"
    )
    parser.add_argument(
        "-t",
        "--tree",
        help="List all Groups and Datasets recursively as tree",
        action="store_true",
    )
    parser.add_argument(
        "-p", "--plain", help="Disable pretty printing", action="store_true"
    )
    parser.add_argument(
        "-d", "--debug", help="Enable debug logging", action="store_true"
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            level=0,
            format="%(asctime)s: [%(levelname)s] - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join("hdf5viewer.log")),
                logging.StreamHandler(sys.stdout),
            ],
            force=True,
        )
    else:
        logging.basicConfig(
            level=20,
            format="%(asctime)s: [%(levelname)s] - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
            force=True,
        )

    if args.export is not None or any([args.list, args.tree]):
        parse_cli_args(args)
    else:
        logging.info("Starting as gui")
        app = QApplication(sys.argv)
        app.setOrganizationName("HDF5Viewer")
        app.setApplicationName("HDF5ViewerPython")
        main_win = MainWindow(init_file_path=pathlib.Path(args.filename))
        main_win.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
