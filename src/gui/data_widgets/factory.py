import pathlib
from typing import Any

import h5py
import numpy as np
from PyQt6.QtWidgets import QTableView, QWidget

from src.gui.table_model import DataTable
from src.lib_h5.dataset_types import H5DatasetType

from .array_plot import ArrayPlotWidget
from .image_view import DataImageRGBView, DataImageView
from .text_browser import DataTextBrowser, FileTextBrowser, GroupTextBrowser


class DataWidgetFactory:

    @classmethod
    def get_data_from_selection(
        cls, file_path: pathlib.Path, object_path: str, plot_type: str
    ) -> tuple[H5DatasetType, Any]:
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
            data_type = H5DatasetType.File
            return data_type, data

        with h5py.File(file_path, "r") as file:
            h5_obj = file[object_path]
            if isinstance(h5_obj, h5py.Group):
                data = np.array([name for name in file[object_path]])
                data_type = H5DatasetType.Group
                return data_type, data

            if isinstance(h5_obj, h5py.Dataset):
                data = np.array(file[object_path])
                if plot_type and plot_type != "Auto":
                    data_type = H5DatasetType.from_string(plot_type)
                else:
                    data_type = H5DatasetType.from_numpy_array(data)
                return data_type, data

        raise ValueError

    @classmethod
    def get_data_widget_from_data(cls, cur_file, cur_obj_path, plot_type) -> QWidget:
        data_type, data = cls.get_data_from_selection(cur_file, cur_obj_path, plot_type)

        if data_type == H5DatasetType.Array1D:
            return ArrayPlotWidget(data)

        if data_type == H5DatasetType.Array2D:
            return DataImageView(data)

        if data_type == H5DatasetType.Table:
            new_widget = QTableView()
            model = DataTable(data)
            new_widget.setModel(model)
            return new_widget

        if data_type == H5DatasetType.ImageRGB:
            return DataImageRGBView(data)

        if data_type == H5DatasetType.String:
            return DataTextBrowser(data)

        if data_type == H5DatasetType.File:
            return FileTextBrowser(data)

        if data_type == H5DatasetType.Group:
            return GroupTextBrowser(data)

        raise ValueError
