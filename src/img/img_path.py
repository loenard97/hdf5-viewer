"""Image path utils."""

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

import logging
import pathlib
import sys


def img_path() -> pathlib.Path:
    """
    Get path to img directory
    """
    if getattr(sys, "frozen", False):
        path = pathlib.Path(sys.executable).parent
        path = pathlib.Path(path, "_internal", "img")
    else:
        path = pathlib.Path(__file__).absolute().parent

    logging.info(f"Image path '{path}'")

    return path
