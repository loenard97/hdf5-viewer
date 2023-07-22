"""Test cli output."""

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
