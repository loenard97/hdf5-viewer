import h5py

from hdf5viewer.h5types.dataset import H5Dataset


class H5File:

    def __init__(self, file_path: str):
        self._file_path = file_path

    def __repr__(self):
        return f"<H5 File '{self._file_path}'>"

    def __getitem__(self, index):
        if not isinstance(index, str):
            raise IndexError
        with h5py.File(self._file_path, 'r') as file:
            if index not in file:
                raise IndexError
        return H5Dataset(self._file_path, index)

    @property
    def tree_view(self):
        return None
