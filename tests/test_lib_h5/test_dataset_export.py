import os
import h5py
import pytest


def test_tmp_test_export_files(tmp_test_export_file):
    if not os.path.exists(tmp_test_export_file):
        pytest.exit("Temporary h5file does not exist")


def test_export_groups(tmp_test_file, tmp_test_export_file):
    with h5py.File(tmp_test_file, 'r') as h5file:
        for group in h5file:
            assert os.path.isdir(os.path.join(tmp_test_export_file, group))


@pytest.mark.skip(reason="TODO: implement recursion")
def test_export_datasets(tmp_test_file, tmp_test_export_file):
    with h5py.File(tmp_test_file, 'r') as h5file:
        for group in h5file:
            for dataset in h5file[group]:
                with open(os.path.join(tmp_test_export_file, group, dataset)) as out_file:
                    assert out_file.read() != "Could not save this Dataset.", f"{group}/{dataset} not exported"
