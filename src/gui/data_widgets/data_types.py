"""Data type classification."""

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

from enum import Enum, auto

import numpy.typing as npt


class DataType(Enum):
    """Enum representing the type of data in a dataset."""

    UNKNOWN = auto()
    STRING = auto()
    ARRAY_1D = auto()
    ARRAY_2D = auto()
    RGB_IMAGE = auto()
    TABLE = auto()
    H5_FILE = auto()
    H5_GROUP = auto()

    @classmethod
    def from_string(cls, plot_type: str) -> "DataType":
        """Construct type from string."""
        registry = {
            "String": cls.STRING,
            "Array1D": cls.ARRAY_1D,
            "Array2D": cls.ARRAY_2D,
            "Table": cls.TABLE,
            "ImageRGB": cls.RGB_IMAGE,
        }

        return registry.get(plot_type, cls.STRING)

    @classmethod
    def from_numpy_array(cls, array: npt.NDArray) -> "DataType":
        """Construct type from numpy array."""
        arr_type = str(array.dtype)
        arr_shape = len(array.shape)
        arr_size = array.size
        max_table_size = 100
        dimensions_array = 1
        dimensions_table = 2
        dimensions_rgb_image = 3

        if arr_shape == dimensions_array and ("int" in arr_type or "float" in arr_type):
            return cls.ARRAY_1D

        if arr_shape == dimensions_table and ("int" in arr_type or "float" in arr_type) and arr_size < max_table_size:
            return cls.TABLE

        if arr_shape == dimensions_rgb_image and ("int" in arr_type or "float" in arr_type):
            return cls.RGB_IMAGE

        return cls.STRING
