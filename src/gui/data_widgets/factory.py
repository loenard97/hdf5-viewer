"""Data Widget Factory that creates correct DataWidget to plot HDF5 file data depending on data type."""

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

import pathlib

import h5py
import numpy as np
import numpy.typing as npt
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget

from src.gui.data_widgets.array_plot import DataWidget1DArray
from src.gui.data_widgets.data_types import DataType
from src.gui.data_widgets.image_view import DataWidget2DImage, DataWidget3DRGBImage
from src.gui.data_widgets.table_view import DataWidget2DTable
from src.gui.data_widgets.text_browser import DataWidgetFileText, DataWidgetGroupText, DataWidgetText


class DataWidgetFactory:
    """Data Widget Factory."""

    @classmethod
    def get_data_from_selection(
        cls,
        file_path: pathlib.Path,
        object_path: str,
        plot_type: str,
    ) -> tuple[DataType, npt.NDArray | pathlib.Path]:
        """
        Figure out which type of data and the data itself that should be plotted next.

        :param pathlib.Path file_path: HDF5 File path to read from
        :param str object_path: Path inside the HDF5 file which Group or Dataset to plot
        :param str plot_type: Type of plot that is requested

        Gets called when user clicks on an entry in the table.
        """
        # only file selected, but not any object inside the file
        if not object_path:
            data = file_path
            data_type = DataType.H5_FILE
            return data_type, data

        with h5py.File(file_path, "r") as file:
            h5_obj = file[object_path]
            if isinstance(h5_obj, h5py.Group):
                data = np.array(list(file[object_path]))
                data_type = DataType.H5_GROUP
                return data_type, data

            if isinstance(h5_obj, h5py.Dataset):
                data = np.array(file[object_path])
                if plot_type and plot_type != "Auto":
                    data_type = DataType.from_string(plot_type)
                else:
                    data_type = DataType.from_numpy_array(data)
                return data_type, data

        raise ValueError

    @classmethod
    def get_data_widget_from_data(
        cls,
        cur_file: pathlib.Path,
        cur_obj_path: str,
        plot_type: str,
    ) -> QWidget | pg.PlotWidget | pg.ImageView:
        """Construct new Data Widget."""
        data_type, data = cls.get_data_from_selection(cur_file, cur_obj_path, plot_type)

        registry = {
            DataType.ARRAY_1D: DataWidget1DArray,
            DataType.ARRAY_2D: DataWidget2DImage,
            DataType.TABLE: DataWidget2DTable,
            DataType.RGB_IMAGE: DataWidget3DRGBImage,
            DataType.STRING: DataWidgetText,
            DataType.H5_FILE: DataWidgetFileText,
            DataType.H5_GROUP: DataWidgetGroupText,
        }
        new_widget = registry[data_type]

        return new_widget(data)
