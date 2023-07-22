"""Dataset type classification."""

from enum import Enum, auto

import numpy.typing as npt


class H5DatasetType(Enum):
    """Enum representing the type of data in a dataset."""

    Unknown = auto()
    String = auto()
    Array1D = auto()
    Array2D = auto()
    ImageRGB = auto()
    Table = auto()

    @classmethod
    def from_string(cls, plot_type: str) -> "H5DatasetType":
        """Construct type from string."""
        match plot_type:
            case "String":
                return cls.String
            case "Array1D":
                return cls.Array1D
            case "Array2D":
                return cls.Array2D
            case "Table":
                return cls.Table
            case "ImageRGB":
                return cls.ImageRGB
            case _:
                return cls.String

    @classmethod
    def from_numpy_array(cls, array: npt.NDArray) -> "H5DatasetType":
        """Construct type from numpy array."""
        arr_type = str(array.dtype)
        arr_shape = len(array.shape)
        arr_size = array.size

        if arr_shape == 1 and ("int" in arr_type or "float" in arr_type):
            return cls.Array1D

        if (
            arr_shape == 2
            and ("int" in arr_type or "float" in arr_type)
            and arr_size < 100
        ):
            return cls.Table

        if arr_shape == 3 and ("int" in arr_type or "float" in arr_type):
            return cls.ImageRGB

        return cls.String
