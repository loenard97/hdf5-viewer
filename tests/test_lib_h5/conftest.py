"""Test H5 file handling."""

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

import h5py
import numpy as np
import pytest

from hdf5viewer.lib_h5.file_export import export_file


@pytest.fixture
def tmp_test_file(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create temporary h5 file for testing."""
    target_output = os.path.join(tmp_path, "h5file.h5")
    with h5py.File(target_output, "w") as file:
        # ----- Types ------ #
        file.create_group("Types")
        # file.create_dataset("Types/String", data="String")
        # file.create_dataset("Types/UTF-8", data="String".encode('utf-8'))
        # file.create_dataset("Types/ASCII", data="String".encode('ascii'))
        # file.create_dataset("Types/Bytes", data=b"Bytes")
        # file.create_dataset("Types/Integer", data=1)
        # file.create_dataset("Types/Float", data=1.1)
        # file.create_dataset("Types/Bool", data=True)
        file.create_dataset("Types/List", data=[])

        # ----- List ------ #
        file.create_group("List")
        file.create_dataset("List/String", data=["String"])
        file.create_dataset("List/UTF-8", data=["String".encode("utf-8")])
        file.create_dataset("List/ASCII", data=["String".encode("ascii")])
        file.create_dataset("List/Bytes", data=[b"Bytes"])
        file.create_dataset("List/Integer", data=[1])
        file.create_dataset("List/Float", data=[1.1])
        file.create_dataset("List/Bool", data=[True])
        file.create_dataset("List/List", data=[[]])

        # ----- Dictionary ------ #
        file.create_group("Dictionary")
        # file.create_dataset("Dictionary/dict", data={'a': 1, 'b': 2})

        # ----- Enumerated Types ------ #
        file.create_group("Enums")
        # dt = h5py.enum_dtype({"RED": 0, "GREEN": 1, "BLUE": 42}, basetype='i')
        # print(h5py.check_enum_dtype(dt))
        # file.create_dataset("Enums/Enum", data=dt)

        # ----- Array1D ------ #
        file.create_group("Array1D")
        file.create_dataset("Array1D/Integer", data=[1, 2, 3, 4, 5])
        file.create_dataset("Array1D/Float", data=[1.1, 2.2, 3.3, 4.4, 5.5])

        # ----- Numpy Arrays ------ #
        file.create_group("Numpy Arrays")
        file.create_group("Numpy Arrays/String")

        file.create_dataset(
            "Numpy Arrays/String/S",
            data=np.array(["First Item", "Second Item"], dtype="S"),
        )
        file.create_dataset(
            "Numpy Arrays/String/a",
            data=np.array(["First Item", "Second Item"], dtype="a"),
        )
        # file.create_dataset("Numpy Arrays/Array of Bytes", data=np.array(["First Item", "Second Item"], dtype='U'))

        file.create_group("Numpy Arrays/Integer")
        file.create_dataset(
            "Numpy Arrays/Integer/int16", data=np.array([1, 2, 3, 4, 5], dtype="int16")
        )
        file.create_dataset(
            "Numpy Arrays/Integer/int32", data=np.array([1, 2, 3, 4, 5], dtype="int32")
        )
        file.create_dataset(
            "Numpy Arrays/Integer/int64", data=np.array([1, 2, 3, 4, 5], dtype="int64")
        )
        file.create_dataset(
            "Numpy Arrays/Integer/uint16",
            data=np.array([1, 2, 3, 4, 5], dtype="uint16"),
        )
        file.create_dataset(
            "Numpy Arrays/Integer/uint32",
            data=np.array([1, 2, 3, 4, 5], dtype="uint32"),
        )
        file.create_dataset(
            "Numpy Arrays/Integer/uint64",
            data=np.array([1, 2, 3, 4, 5], dtype="uint64"),
        )
        # file.create_dataset("Numpy Arrays/Array of 128-bit Integer", data=np.array([1, 2, 3, 4, 5], dtype='int128'))

        file.create_group("Numpy Arrays/Float")
        file.create_dataset(
            "Numpy Arrays/Float/float16",
            data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype="float16"),
        )
        file.create_dataset(
            "Numpy Arrays/Float/float32",
            data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype="float32"),
        )
        file.create_dataset(
            "Numpy Arrays/Float/float64",
            data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype="float64"),
        )

    return pathlib.Path(target_output)


@pytest.fixture
def tmp_test_export_file(tmp_path: pathlib.Path) -> pathlib.Path:
    """Test file export."""
    export_file(
        pathlib.Path(r"E:\Projekte\Python\hdf5viewer\test.h5"),
        pathlib.Path(tmp_path),
        "csv",
    )
    return tmp_path
