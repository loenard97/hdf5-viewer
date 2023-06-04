import os
import pathlib

import h5py
import numpy as np

from hdf5viewer.lib_h5.dataset_types import H5DatasetType


def export_file(input_file: pathlib.Path, output_file: pathlib.Path, save_as_type: str):
    """
    Export HDF5 File
    :param pathlib.Path input_file: Path to H5 file
    :param pathlib.Path output_file: Path to export to
    :param str save_as_type: File type
    """
    with h5py.File(input_file, 'r') as file:
        ds = [d for d in file if isinstance(file[d], h5py.Dataset)]
        gs = [g for g in file if isinstance(file[g], h5py.Group)]

    for g in gs:
        export_group(input_file, g, output_file, save_as_type)
    for d in ds:
        export_dataset(input_file, d, output_file, save_as_type)


def export_group(input_file: pathlib.Path, group: str, output_file: pathlib.Path, save_as_type: str):
    """
    Export HDF5 Group
    :param pathlib.Path input_file: File path to H5 file
    :param str group: Group in H5 file to export
    :param pathlib.Path output_file: File name to export to
    :param str save_as_type: File type
    """
    with h5py.File(input_file, 'r') as file:
        ds = [d for d in file[group] if isinstance(file[group][d], h5py.Dataset)]
        gs = [g for g in file[group] if isinstance(file[group][g], h5py.Group)]

    for g in gs:
        export_group(input_file, group + '/' + g, output_file, save_as_type)
    for d in ds:
        export_dataset(input_file, group + '/' + d, output_file, save_as_type)


def export_dataset(input_file: pathlib.Path, dataset: str, output_file: pathlib.Path, save_as_type: str):
    """
    Export HDF5 Dataset
    :param pathlib.Path input_file: File path to H5 file
    :param str dataset: Dataset in H5 file to export
    :param pathlib.Path output_file: File name to export to
    :param str save_as_type: File type
    """
    os.makedirs(output_file.parent, exist_ok=True)

    with h5py.File(input_file, 'r') as file:
        array = np.array(file[dataset])
    ds_type = H5DatasetType.from_numpy_array(array)

    if save_as_type == 'csv':
        if ds_type == H5DatasetType.String:
            try:
                with open(output_file, 'w') as file_str:
                    for e in array:
                        if isinstance(e, bytes):
                            file_str.write(e.decode())
                        elif isinstance(e, np.bool_):
                            file_str.write(str(e))
                        else:
                            print("unknown")
            except (TypeError, PermissionError) as err:
                print(f"skipping file write {output_file}, {err}, {ds_type}, {array}")
            else:
                return

        # np.savetxt(fname=arr_path, X=array, delimiter=',', newline='\n', fmt='%.0f')
        try:
            np.savetxt(output_file, array, delimiter=",")
        except BaseException as err:
            print(f"skipping np.savetxt {output_file}, {err}, {ds_type}, {array}")

    elif save_as_type == 'npy':
        np.save(file=output_file, arr=array)

    else:
        print("unknown file type")
        with open(output_file, 'w') as err_file:
            err_file.write("Could not save this Dataset.")
