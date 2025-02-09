"""Script that generates a test .h5 file used for testing."""

import pathlib

import h5py
import numpy as np

DIR = pathlib.Path(__file__).parent


def main() -> None:
    """Generate .h5 file."""
    with h5py.File(pathlib.Path(DIR, "test_file.h5"), "w") as file:
        # normal np arrays
        file.create_dataset("Array1D/Float", data=np.array([0.1, 0.2, 0.3, 0.4, 0.5]))
        file.create_dataset("Array1D/Integer", data=np.array([1, 2, 3, 4, 5]))

        # raveled np arrays
        file.create_dataset(
            "Array1D/ColumnVector", data=np.array([[1], [2], [3], [4], [5]])
        )
        file.create_dataset("Array1D/RowVector", data=np.array([[1, 2, 3, 4, 5]]))
        file.create_dataset(
            "Array1D/LongRowVector", data=np.array([[i for i in range(150)]])
        )


if __name__ == "__main__":
    main()
