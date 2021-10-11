import subprocess

import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class SnpphenaDownloader(DownloadBase):
    """Downloader class for the BC5DR data."""

    DATASET_NAME = "SNPPhenA"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "http://nil.fdi.ucm.es/sites/default/files/SNPPhenA.zip"
    LOGGER = logger

    def _download(self) -> None:
        self.LOGGER.info("Downloading the {} database...".format(self.DATASET_NAME))
        outfile = self.download_location / "SNPPhenA.zip"
        wget.download(self.DOWNLOAD_URL, str(outfile))

        self.LOGGER.info("Unzipping the database.")
        subprocess.call("unzip {}".format(outfile))

    def _process(self) -> None:
        pass


if __name__ == "__main__":
    SnpphenaDownloader("../../data/snpphena").download()
