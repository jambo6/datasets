import os
import subprocess

import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class DisgenetDownloader(DownloadBase):
    """Downloader class for the DisGeNET data."""

    DATASET_NAME = "DisGeNet"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "https://www.disgenet.org/download/sqlite/current/2020"
    LOGGER = logger

    def _download(self) -> None:
        # Type is gzip
        self.LOGGER.info("Downloading the DisGeNet database...")
        outfile = self.download_location / "disgenet.db.gz"
        wget.download(self.DOWNLOAD_URL, str(outfile))

        # Call gunzip
        self.LOGGER.info("Unzipping the database.")
        subprocess.call("gunzip {}".format(outfile))

        # Unzip then remove the zipfile
        os.remove(outfile)

    def _process(self) -> None:
        self.LOGGER.warning("No processing methods exist for DisGeNet, skipping.")
