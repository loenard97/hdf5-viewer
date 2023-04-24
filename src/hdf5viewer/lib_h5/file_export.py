import os
import h5py
import numpy as np


def save_file_to_file(in_path, out_path, file_type):
    print(f"save file {in_path=}, {out_path=}")
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
        save_group_to_file(in_path, "", group, out_path, file_type)

    for dataset in datasets:
        save_dataset_to_file(in_path, "", dataset, out_path, file_type)


def save_group_to_file(in_path, parent_path, group_path, out_path, file_type):
    print(f"save group {in_path=}, {group_path=}, {out_path=}")
    cur_path = '/'.join([parent_path, group_path])
    os.makedirs(os.path.join(cur_path), exist_ok=True)

    groups = []
    datasets = []
    with h5py.File(in_path, 'r') as file:
        for name in file[cur_path]:
            if isinstance(file[cur_path][name], h5py.Group):
                groups.append(name)
            elif isinstance(file[cur_path][name], h5py.Dataset):
                datasets.append(name)

    for group in groups:
        save_group_to_file(in_path, cur_path, group, out_path, file_type)

    for dataset in datasets:
        save_dataset_to_file(in_path, cur_path, dataset, out_path, file_type)


def save_dataset_to_file(in_path, parent_path, dataset_path, out_path: str, file_type):
    """
    save dataset to file
    :param array: Dataset as numpy array
    :param str file_path: save file path
    """
    cur_path = '/'.join([parent_path, dataset_path])
    arr_path = os.path.join(out_path, *cur_path.split('/'))
    print(f"save dataset {in_path=}, {parent_path=}, {dataset_path=}, {out_path=}, {cur_path=}, {arr_path=}")

    with h5py.File(in_path, 'r') as file:
        array = np.array(file[cur_path])

    if file_type == 'csv':
        # np.savetxt(fname=arr_path, X=array, delimiter=',', newline='\n', fmt='%.0f')
        try:
            np.savetxt(arr_path, array, delimiter=",", fmt='%d')
        except BaseException:
            print(f"skipping {arr_path}")

    elif file_type == 'npy':
        np.save(file=arr_path, arr=array)

    else:
        print("unknown file type")


def main():
    save_file_to_file(r"E:\Projekte\Python\hdf5viewer\test.h5", r"E:\Projekte\Python\hdf5viewer\out", 'csv')


if __name__ == '__main__':
    main()
