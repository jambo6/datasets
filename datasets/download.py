from pathlib import Path

import datasets


class DatasetNotFoundError(Exception):
    pass


def download(dataset_name: str, download_location: str) -> None:
    """Downloads a specified dataset to a given location.

    Arguments:
        dataset_name: The name of the dataset to download.
        download_location: The location to download the dataset to. Note that `dataset_name` will automatically be
            appended to the location string.
    """
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
