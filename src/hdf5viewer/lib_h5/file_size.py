"""File size formatting util."""

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


def file_size_to_str(file_path: str) -> str:
    """Get formatted file size."""
    size = os.path.getsize(file_path)

    if size > 1024**3:
        return f"{size/1024**3:.2f} GB"
    elif size > 1024**2:
        return f"{size/1024**2:.2f} MB"
    elif size > 1024:
        return f"{size/1024:.2f} kB"
    else:
        return f"{size} bytes"
