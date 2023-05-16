import h5py


def recursive_h5(file_path):
    item_list = []
    with h5py.File(file_path, 'r') as file:
        for i, (name, obj) in enumerate(file.items()):
            is_last = i == len(file) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, 0, is_last))
                for e in recursive_group(file_path, f"{name}", 1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", 0, is_last))

    return item_list


def recursive_group(file_path, group, depth):
    item_list = []
    with h5py.File(file_path, 'r') as file:
        for i, (name, obj) in enumerate(file[group].items()):
            is_last = i == len(file[group]) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, depth, is_last))
                for e in recursive_group(file_path, f"{group}/{name}", depth+1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", depth, is_last))

    return item_list
