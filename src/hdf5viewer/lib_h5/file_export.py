import os
import h5py
import numpy as np

from hdf5viewer.lib_h5.dataset_types import H5DatasetType


def export_h5file(in_path, out_path, file_type):
    """
    Export HDF5 File
    :param str in_path: h5 file path
    :param str out_path: export path
    :param str file_type: export file type
    """
    os.makedirs(out_path, exist_ok=True)

    groups = []
    datasets = []
    with h5py.File(in_path, 'r') as file:
        for name in file:
            if isinstance(file[name], h5py.Group):
                groups.append(name)
            elif isinstance(file[name], h5py.Dataset):
                datasets.append(name)

    for group in groups:
        export_h5group(in_path, "", group, out_path, file_type)

    for dataset in datasets:
        export_h5dataset(in_path, "", dataset, out_path, file_type)


def export_h5group(in_path, parent_path, group_path, out_path, file_type):
    """
    Export HDF5 Group
    :param str in_path: h5 file path
    :param str parent_path: path to parent object
    :param str group_path: path to group
    :param str out_path: export path
    :param str file_type: export file type
    """
    cur_path = '/'.join([parent_path, group_path]).removeprefix('/')
    os.makedirs(os.path.join(out_path, cur_path), exist_ok=True)

    groups = []
    datasets = []
    with h5py.File(in_path, 'r') as file:
        for name in file[cur_path]:
            if isinstance(file[cur_path][name], h5py.Group):
                groups.append(name)
            elif isinstance(file[cur_path][name], h5py.Dataset):
                datasets.append(name)

    for group in groups:
        export_h5group(in_path, cur_path, group, out_path, file_type)

    for dataset in datasets:
        export_h5dataset(in_path, cur_path, dataset, out_path, file_type)


def export_h5dataset(in_path, parent_path, dataset_path, out_path, file_type):
    """
    Export HDF5 Group
    :param str in_path: h5 file path
    :param str parent_path: path to parent object
    :param str dataset_path: path to dataset
    :param str out_path: export path
    :param str file_type: export file type
    """
    cur_path = '/'.join([parent_path, dataset_path])
    arr_path = os.path.join(out_path, *cur_path.split('/'))

    with h5py.File(in_path, 'r') as file:
        array = np.array(file[cur_path])

    ds_type = H5DatasetType.from_numpy_array(array)

    if file_type == 'csv':
        if ds_type == H5DatasetType.String:
            with open(arr_path, 'w') as file_str:
                try:
                    for e in array:
                        if isinstance(e, bytes):
                            file_str.write(e.decode())
                        elif isinstance(e, np.bool_):
                            file_str.write(str(e))
                        else:
                            print("unknown")
                except TypeError as err:
                    print(f"skipping file write {arr_path}, {err}, {ds_type}, {array}")
                    with open(arr_path, 'w') as err_file:
                        err_file.write("Could not save this Dataset.")
                else:
                    return

        # np.savetxt(fname=arr_path, X=array, delimiter=',', newline='\n', fmt='%.0f')
        try:
            np.savetxt(arr_path, array, delimiter=",")
        except BaseException as err:
            print(f"skipping np.savetxt {arr_path}, {err}, {ds_type}, {array}")
            with open(arr_path, 'w') as err_file:
                err_file.write("Could not save this Dataset.")

    elif file_type == 'npy':
        np.save(file=arr_path, arr=array)

    else:
        print("unknown file type")
        with open(arr_path, 'w') as err_file:
            err_file.write("Could not save this Dataset.")


def main():
    try:
        export_h5file(r"E:\Projekte\Python\hdf5viewer\test.h5", r"E:\Projekte\Python\hdf5viewer\out", 'csv')
    except OSError:
        pass


if __name__ == '__main__':
    main()
