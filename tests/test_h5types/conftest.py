import os
import h5py
import pytest


@pytest.fixture
def create_test_files(tmp_path):
    """
    Create temporary h5 file for testing
    """
    target_output = os.path.join(tmp_path, "h5file.h5")
    with h5py.File(target_output, 'w') as file:
        file.create_dataset("Text", data=["Hello World"])
        file.create_dataset("Array1D", data=[1, 2, 3])
    return target_output
