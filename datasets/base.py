import os
import pprint
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from datasets import common


@dataclass
class DatasetInfo:
    """Information about a dataset.

    `DatasetInfo` documents information about the raw dataset being downloaded, and any processing results that amount
    from class `process` methods.

    Attributes:
        description (str): A description of the dataset.
        processed_description (str, optional): A description of the processed function applied to the raw data.
        citation (str): A BibTeX citation of the dataset.
        homepage (str): A URL to the official homepage for the dataset.
        # raw_size (int, optional): The size of the files to download to generate the dataset, in bytes.
        # processed_size (int, optional): The size of the processed data.
    """

    # Set in the dataset scripts
    description: str = field(default_factory=str)
    processed_description: str = field(default_factory=str)
    citation: str = field(default_factory=str)
    homepage: str = field(default_factory=str)
    licence: str = field(default_factory=str)


class DownloadBase(ABC):
    """Base class for download functionality."""

    DATASET_NAME: str
    MODULE_DIR: Path

    def __init__(self, download_location: Path) -> None:
        # Location to dump the raw data
        self.dataset_info = DatasetInfo(**common.load_json(self.MODULE_DIR / "dataset_info.json"))
        self.download_location = download_location

        # Location to save any processed data
        self.processed_location = download_location / "processed"

    def __repr__(self) -> str:
        return pprint.pformat(self.dataset_info.__dict__)

    def download(self) -> None:
        """Acts as a decorator around the _download function."""
        logger.info("Dataset information:\n{}".format(self))
        logger.info(
            "Beginning download of {} data. This will be saved in {}.".format(self.DATASET_NAME, self.download_location)
        )

        # Check not exists
        if os.path.isdir(self.download_location):
            logger.warning(
                "Folder already exists at {} and so the download step is being skipped. Remove this folder to "
                "redownload.".format(self.download_location)
            )
            return None

        # Make directory
        common.make_directory_if_not_exists(self.download_location)

        self._download()

    def process(self) -> None:
        """Acts as a decorator around the _process function."""
        logger.info("Beginning processing of the {} dataset.".format(self.DATASET_NAME))

        # Check not exists
        if os.path.isdir(self.processed_location):
            logger.warning(
                "Folder already exists at {} and so the download step is being skipped. Remove this folder to "
                "reprocess.".format(self.processed_location)
            )
            return None

        # Otherwise make
        common.make_directory_if_not_exists(self.processed_location)

        self._process()

    @abstractmethod
    def _download(self) -> None:
        pass

    @abstractmethod
    def _process(self) -> None:
        pass
