"""Recursive iterators for files and groups."""

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


def recursive_h5(file_path: pathlib.Path) -> list[tuple[str, int, bool]]:
    """Iterate recursively through file."""
    item_list = []
    with h5py.File(file_path, "r") as file:
        for i, (name, obj) in enumerate(file.items()):
            is_last = i == len(file) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, 0, is_last))
                for e in recursive_group(file_path, f"{name}", 1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", 0, is_last))

    return item_list


def recursive_group(
    file_path: pathlib.Path, group: str, depth: int
) -> list[tuple[str, int, bool]]:
    """Iterate recursively through group."""
    item_list = []
    with h5py.File(file_path, "r") as file:
        for i, (name, obj) in enumerate(file[group].items()):
            is_last = i == len(file[group]) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, depth, is_last))
                for e in recursive_group(file_path, f"{group}/{name}", depth + 1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", depth, is_last))

    return item_list
