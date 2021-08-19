import os
import zipfile
from io import BytesIO
from urllib.request import urlopen

import numpy as np
import processors

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class Physionet2019Downloader(DownloadBase):
    """Downloader class for the DisGeNET data."""

    DATASET_NAME = "physionet2019"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "https://archive.physionet.org/users/shared/challenge-2019"
    LOGGER = logger

    DOWNLOAD_URL_APPEND = ["training_setA.zip", "training_setB.zip"]

    def _download(self) -> None:
        self.LOGGER.info("Downloading the PhysioNet2019 data...")
        for name in self.DOWNLOAD_URL_APPEND:
            self.LOGGER.info("Downloading {}".format(name))

            url = "{}/{}".format(self.DOWNLOAD_URL, name)
            r = urlopen(url)
            z = zipfile.ZipFile(BytesIO(r.read()))
            z.extractall(self.download_location)

        # Training set A gets saved as training, this is just to explicitly note it is set A
        os.rename(self.download_location / "training", self.download_location / "training_setA")

    def _process(self) -> None:
        # Load all data into a big datafarme
        frame = processors.load_to_dataframe(self.download_location)

        # Convert to numpy data and labels
        data, labels, columns = processors.convert_to_numpy_format(frame)

        np.savez(
            self.processed_location / "data.npz",
            data=np.array(data, dtype=object),
            labels=np.array(labels, dtype=object),
            columns=columns,
        )
