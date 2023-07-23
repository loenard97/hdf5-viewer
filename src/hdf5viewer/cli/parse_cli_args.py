"""Cli components."""

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

import os
import pathlib
from argparse import Namespace

import h5py

from hdf5viewer.cli.styling import color
from hdf5viewer.lib_h5.recursive_iterator import recursive_h5


def parse_cli_args(args: Namespace) -> None:
    """Parse cli arguments."""
    if not args.filename:
        print(f"{color('Application error', 'red')}: No input file given. Use")
        print("  $ hdf5-viewer --help")
        print("for a list of supported arguments.")
        return

    if args.tree:
        print(list_tree_file_items(args.filename, args.plain))

    elif args.list:
        print(list_file_items(args.filename, args.plain))

    elif args.export:
        print(f"{color('Application error', 'red')}: Exporting is not implemented yet")


def list_file_items(in_path: pathlib.Path, plain: bool) -> str:
    """List items in file as list."""
    # TODO: reformat as table
    ret = []
    if not plain:
        ret.append("─" * os.get_terminal_size()[0])
        ret.append(f"  {color('File', 'green')}: {in_path}")
        ret.append("─" * os.get_terminal_size()[0])

    with h5py.File(in_path, "r") as file:
        for i, name in enumerate(file):
            is_last = i == len(file) - 1
            if not plain:
                ret.append(f"  {'└' if is_last else '├'}─ {name}")
            else:
                ret.append(f"{name}")

    return "\n".join(ret)


def list_tree_file_items(in_path: pathlib.Path, plain: bool) -> str:
    """List items in file as tree recursively."""
    ret = []
    if not plain:
        ret.append("─" * os.get_terminal_size()[0])
        ret.append(f"  {color('File', 'green')}: {in_path}")
        ret.append("─" * os.get_terminal_size()[0])

    for name, depth, is_last in recursive_h5(in_path):
        if not plain:
            ret.append(f"  {'│  ' * depth}{'└' if is_last else '├'}─ {name}")
        else:
            ret.append(f"{'  ' * depth}{name}")

    return "\n".join(ret)
