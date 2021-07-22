from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class PubtatorDownloader(DownloadBase):
    """Downloader class for the PubTator database."""

    DATASET_NAME = "PubTator"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = ""
    LOGGER = logger

    def _download(self) -> None:
        pass

    def _process(self) -> None:
        pass
