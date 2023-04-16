import h5py
import numpy as np
from enum import Enum, auto


class H5DatasetType(Enum):
    Unknown = auto()
    Text = auto()
    Array1D = auto()
    Array2D = auto()
    ImageRGB = auto()
    Table = auto()

    @classmethod
    def from_numpy_array(cls, array):
        print(array.dtype, len(array.shape), array.size)
        match array.dtype, len(array.shape), array.size:
            case arr_type, _, _ if str(arr_type).startswith("|S"):
                return cls.Text
            case "int32" | "int64" | "float32" | "float64", 1, _:
                return cls.Array1D
            case "int32" | "int64" | "float32" | "float64", 2, _:
                return cls.Array2D
            case "int32" | "int64" | "float32" | "float64", 2, size if size < 100:
                return cls.Table
            case "int32" | "int64" | "float32" | "float64", 3, _:
                return cls.ImageRGB
            case _:
                return cls.Unknown


class H5Dataset:

    def __init__(self, file_path: str, dataset_path: str):
        self._file_path = file_path
        self._dataset_path = dataset_path

    def __repr__(self):
        return f"<H5 Dataset '{self._dataset_path}'>"

    @property
    def _data(self):
        """
        get data as numpy array
        """
        with h5py.File(self._file_path, 'r') as file:
            return np.array(file[self._dataset_path])

    @property
    def dtype(self):
        """
        get dataset type
        """
        return H5DatasetType.from_numpy_array(self._data)

    def save_to_file(self, file_path: str):
        """
        save dataset to file
        :param str file_path: save file path
        """
        file_type = file_path.split('.')[-1]

        if file_type == 'csv':
            np.savetxt(fname=file_path, X=self._data, delimiter=',', newline='\n', fmt='%.0f')

        elif file_type == 'npy':
            np.save(file=file_path, arr=self._data)
