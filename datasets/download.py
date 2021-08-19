import os.path
from pathlib import Path
from typing import Optional, Union

import datasets


class DatasetNotFoundError(Exception):
    pass


class NotAbsolutePathError(Exception):
    HELP = (
        "If you are using relative paths from the current file, try using "
        "\n\t`Path(__file__).parents[1] / 'my_loation'`"
        "\nwhere `Path` is imported from the `pathlib` module."
    )

    def __init__(self, message: Optional[str]) -> None:
        self.message = message

    def __str__(self) -> str:
        if self.message:
            return "{}\n{}".format(self.message, self.HELP)
        else:
            return self.HELP


def download(dataset_name: str, download_location: Union[Path, str]) -> None:
    """Downloads a specified dataset to a given location.

    Arguments:
        dataset_name: The name of the dataset to download.
        download_location: The location to download the dataset to. Note that `dataset_name` will automatically be
            appended to the location string. This path must be absolute.
    """
    # Only allow
    if not os.path.isabs(download_location):
        raise NotAbsolutePathError("{} is relative, required absolute path.".format(download_location))

    # Get the dataset downloader class if given a valid dataset.
    downloader_class = datasets.DATASETS.get(dataset_name)
    if not downloader_class:
        raise DatasetNotFoundError(
            "Dataset {} not found, must be one of: {}.".format(dataset_name, datasets.DATASETS.keys())
        )

    # Make dirs
    base_folder = Path(download_location) / dataset_name

    # Perform the download functions
    downloader = downloader_class(download_location=base_folder)
    downloader.download()
    downloader.process()
