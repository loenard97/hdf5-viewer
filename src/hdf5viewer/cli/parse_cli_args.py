import os
import h5py

from hdf5viewer.cli.styling import color
from hdf5viewer.lib_h5.recursive_iterator import recursive_h5


def parse_cli_args(args):
    if args.tree:
        if not args.filename:
            print("No file given.")
            return
        list_tree_file_items(args.filename, args.plain)

    elif args.list:
        if not args.filename:
            print("No file given.")
            return
        list_file_items(args.filename, args.plain)

    elif args.export:
        print("Not implemented")


def list_file_items(in_path: str, pretty_printing: bool):
    if not pretty_printing:
        print("─" * os.get_terminal_size()[0])
        print(f"  {color('File', 'green')}: {in_path}")
        print("─" * os.get_terminal_size()[0])

    with h5py.File(in_path, 'r') as file:
        for i, name in enumerate(file):
            is_last = i == len(file) - 1
            print(f"  {'└' if is_last else '├'}─ {name}")

    if not pretty_printing:
        print()


def list_tree_file_items(in_path: str, pretty_printing: bool):
    if not pretty_printing:
        print("─" * os.get_terminal_size()[0])
        print(f"  {color('File', 'green')}: {in_path}")
        print("─" * os.get_terminal_size()[0])

    for name, depth, is_last in recursive_h5(in_path):
        print(f"  {'│  ' * depth}{'└' if is_last else '├'}─ {name}")

    if not pretty_printing:
        print()
