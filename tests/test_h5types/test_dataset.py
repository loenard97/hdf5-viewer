import os
import h5py

from hdf5viewer.h5types.file import H5File


def test_create_test_files(create_test_files):
    assert os.path.exists(create_test_files) is True


def test_file(create_test_files):
    file = H5File(create_test_files)
    assert file.tree_view is None


def test_iterate(create_test_files):
    with h5py.File(create_test_files, 'r') as file:
        for name in file:
            assert name in ["Text", "Array1D"]
