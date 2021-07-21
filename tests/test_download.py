import pytest

import datasets.download
from datasets import download


def test_download():
    assert False


def test__check_dataset():
    # Ensure fail on non dataset name
    with pytest.raises(datasets.download.DatasetNotFoundError):
        download._check_dataset("this_isnt_a_dataset")
