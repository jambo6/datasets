import subprocess

from datasets import common
from datasets.base import DownloadBase
from datasets.biobert import processors
from datasets.biobert.processors import logger


class BiobertDownloader(DownloadBase):
    """Downloader class for the BioBert data."""

    DATASET_NAME = "BioBert"
    DOWNLOAD_SCRIPT = "./download.sh"
    MODULE_DIR = common.this_directory(__file__)

    def _download(self) -> None:
        subprocess.check_call(["./download.sh", self.download_location])

    def _process(self) -> None:
        # Make processed look like raw
        logger.info("Performing RE processing...")
        processed_re = self.processed_location / "RE"
        common.make_directory_if_not_exists(processed_re)
        processors.process_re(self.download_location / "RE", processed_re)
        logger.info("RE processing successful.")


if __name__ == "__main__":
    from pathlib import Path

    path = Path("../../data/biobert")
    BiobertDownloader(path).process()
