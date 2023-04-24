import h5py

from src.hdf5viewer.lib_h5.file_export import save_dataset_to_file


def parse_cli_args(args):
    if args.export:
        export_file(args.filename, args.export)


def export_file(in_path, out_path):
    with h5py.File(in_path, 'r') as file:
        for elem in file:
            if isinstance(elem, h5py.Group):
                export_group(in_path, out_path)
            elif isinstance(elem, h5py.Dataset):
                export_dataset(in_path, out_path)


def export_group(in_path, out_path):
    pass


def export_dataset(in_path, out_path):
    pass
