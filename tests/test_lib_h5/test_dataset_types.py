"""Test dataset types."""

import os
import pathlib

import h5py
import numpy as np
import pytest

from hdf5viewer.lib_h5.dataset_types import H5DatasetType


def test_tmp_test_files(tmp_test_file: pathlib.Path) -> None:
    """Test temp file."""
    if not os.path.exists(tmp_test_file):
        pytest.exit("Temporary h5file does not exist")


def test_types(tmp_test_file: pathlib.Path) -> None:
    """Test types."""
    with h5py.File(tmp_test_file, "r") as file:
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/String"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/UTF-8"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/ASCII"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/Bytes"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/Integer"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/Float"])) is H5DatasetType.String
        # assert H5DatasetType.from_numpy_array(np.array(file["Types/Bool"])) is H5DatasetType.String
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Types/List"]))
            is H5DatasetType.Array1D
        )


def test_list(tmp_test_file: pathlib.Path) -> None:
    """Test list."""
    with h5py.File(tmp_test_file, "r") as file:
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/String"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/UTF-8"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/ASCII"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/Bytes"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/Integer"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/Float"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/Bool"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["List/List"]))
            is H5DatasetType.Table
        )


def test_dictionary(tmp_test_file: pathlib.Path) -> None:
    """Test dictionary."""
    # with h5py.File(tmp_test_file, 'r') as file:
    pass


def test_enum(tmp_test_file: pathlib.Path) -> None:
    """Test enum."""
    # with h5py.File(tmp_test_file, 'r') as file:
    pass


def test_array1d(tmp_test_file: pathlib.Path) -> None:
    """Test 1D arrays."""
    with h5py.File(tmp_test_file, "r") as file:
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Array1D/Integer"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Array1D/Float"]))
            is H5DatasetType.Array1D
        )


def test_numpy_arrays(tmp_test_file: pathlib.Path) -> None:
    """Test numpy arrays."""
    with h5py.File(tmp_test_file, "r") as file:
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/String/S"]))
            is H5DatasetType.String
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/String/a"]))
            is H5DatasetType.String
        )

        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Integer/int16"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Integer/int32"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Integer/int64"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(
                np.array(file["Numpy Arrays/Integer/uint16"])
            )
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(
                np.array(file["Numpy Arrays/Integer/uint32"])
            )
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(
                np.array(file["Numpy Arrays/Integer/uint64"])
            )
            is H5DatasetType.Array1D
        )

        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Float/float16"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Float/float32"]))
            is H5DatasetType.Array1D
        )
        assert (
            H5DatasetType.from_numpy_array(np.array(file["Numpy Arrays/Float/float64"]))
            is H5DatasetType.Array1D
        )
