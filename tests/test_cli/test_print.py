"""Test cli output."""

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
import pathlib

import pytest

# from hdf5viewer.cli.parse_cli_args import list_file_items


def test_tmp_test_files(tmp_test_file: pathlib.Path) -> None:
    """Test temp files."""
    if not os.path.exists(tmp_test_file):
        pytest.exit("Temporary h5file does not exist")


# def test_list_plain(tmp_test_file):
#     assert list_file_items(tmp_test_file, True) == "Array1D\nDictionary\nEnums\nList\nNumpy Arrays\nTypes"
