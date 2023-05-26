import os
import h5py
import pytest
import numpy as np

from hdf5viewer.lib_h5.file_export import export_h5file


@pytest.fixture
def tmp_test_file(tmp_path):
    """
    Create temporary h5 file for testing
    """
    target_output = os.path.join(tmp_path, "h5file.h5")
    with h5py.File(target_output, 'w') as file:
        # ----- Types ------ #
        file.create_group("Types")
        # file.create_dataset("Types/String", data="String")
        # file.create_dataset("Types/UTF-8", data="String".encode('utf-8'))
        # file.create_dataset("Types/ASCII", data="String".encode('ascii'))
        # file.create_dataset("Types/Bytes", data=b"Bytes")
        # file.create_dataset("Types/Integer", data=1)
        # file.create_dataset("Types/Float", data=1.1)
        # file.create_dataset("Types/Bool", data=True)
        file.create_dataset("Types/List", data=[])

        # ----- List ------ #
        file.create_group("List")
        file.create_dataset("List/String", data=["String"])
        file.create_dataset("List/UTF-8", data=["String".encode('utf-8')])
        file.create_dataset("List/ASCII", data=["String".encode('ascii')])
        file.create_dataset("List/Bytes", data=[b"Bytes"])
        file.create_dataset("List/Integer", data=[1])
        file.create_dataset("List/Float", data=[1.1])
        file.create_dataset("List/Bool", data=[True])
        file.create_dataset("List/List", data=[[]])

        # ----- Dictionary ------ #
        file.create_group("Dictionary")
        # file.create_dataset("Dictionary/dict", data={'a': 1, 'b': 2})

        # ----- Enumerated Types ------ #
        file.create_group("Enums")
        # dt = h5py.enum_dtype({"RED": 0, "GREEN": 1, "BLUE": 42}, basetype='i')
        # print(h5py.check_enum_dtype(dt))
        # file.create_dataset("Enums/Enum", data=dt)

        # ----- Array1D ------ #
        file.create_group("Array1D")
        file.create_dataset("Array1D/Integer", data=[1, 2, 3, 4, 5])
        file.create_dataset("Array1D/Float", data=[1.1, 2.2, 3.3, 4.4, 5.5])

        # ----- Numpy Arrays ------ #
        file.create_group("Numpy Arrays")
        file.create_group("Numpy Arrays/String")

        file.create_dataset("Numpy Arrays/String/S", data=np.array(["First Item", "Second Item"], dtype='S'))
        file.create_dataset("Numpy Arrays/String/a", data=np.array(["First Item", "Second Item"], dtype='a'))
        # file.create_dataset("Numpy Arrays/Array of Bytes", data=np.array(["First Item", "Second Item"], dtype='U'))

        file.create_group("Numpy Arrays/Integer")
        file.create_dataset("Numpy Arrays/Integer/int16", data=np.array([1, 2, 3, 4, 5], dtype='int16'))
        file.create_dataset("Numpy Arrays/Integer/int32", data=np.array([1, 2, 3, 4, 5], dtype='int32'))
        file.create_dataset("Numpy Arrays/Integer/int64", data=np.array([1, 2, 3, 4, 5], dtype='int64'))
        file.create_dataset("Numpy Arrays/Integer/uint16", data=np.array([1, 2, 3, 4, 5], dtype='uint16'))
        file.create_dataset("Numpy Arrays/Integer/uint32", data=np.array([1, 2, 3, 4, 5], dtype='uint32'))
        file.create_dataset("Numpy Arrays/Integer/uint64", data=np.array([1, 2, 3, 4, 5], dtype='uint64'))
        # file.create_dataset("Numpy Arrays/Array of 128-bit Integer", data=np.array([1, 2, 3, 4, 5], dtype='int128'))

        file.create_group("Numpy Arrays/Float")
        file.create_dataset("Numpy Arrays/Float/float16", data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype='float16'))
        file.create_dataset("Numpy Arrays/Float/float32", data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype='float32'))
        file.create_dataset("Numpy Arrays/Float/float64", data=np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype='float64'))

    return target_output


@pytest.fixture
def tmp_test_export_file(tmp_path):
    export_h5file(r"E:\Projekte\Python\hdf5viewer\test.h5", tmp_path, 'csv')
    return tmp_path
