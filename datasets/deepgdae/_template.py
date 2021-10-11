from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class DisgenetDownloader(DownloadBase):
    """Downloader class for the DisGeNET data."""

    DATASET_NAME = "_template"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = ""
    LOGGER = logger

    def _download(self) -> None:
        pass

    def _process(self) -> None:
        pass
