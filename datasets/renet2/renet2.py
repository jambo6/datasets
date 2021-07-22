import os

import pandas as pd
import wget

from datasets import base, common
from datasets.renet2 import processors


class RenetDownloader(base.DownloadBase):
    """Downloader class for the renet data."""

    DATASET_NAME = "RENET2"
    DOWNLOAD_URL: str = "http://www.bio8.cs.hku.hk/RENET2/renet2_data_models.tar.gz"
    MODULE_DIR = common.this_directory(__file__)
    LOGGER = processors.logger

    def _download(self) -> None:
        # Download the tarfile
        outfile = self.download_location / self.DOWNLOAD_URL.split("/")[-1]
        wget.download(self.DOWNLOAD_URL, str(outfile))

        # Open the tarfile
        common.untar(outfile, self.download_location)

        # Delete the original tarfile
        os.remove(outfile)

    def _process(self) -> None:
        # Processed data lives here
        locations = ["abs_data/1st_ann", "abs_data/2nd_ann", "ft_data"]

        for location in locations:
            self.LOGGER.info("Processing {}...".format(location))

            location_directory = self.download_location / "data" / location

            # Load annotations
            annotation_names = ["pmid", "start_idx", "end_idx", "name", "type", "id"]
            annotations = pd.read_csv(
                location_directory / "anns.txt", sep="\t", header=None, usecols=range(6), names=annotation_names
            )

            # Load labels
            labels = pd.read_csv(location_directory / "labels.txt")

            # Load the actual documents
            split_by = "\n\n" if location == "ft_data" else "$$$"
            documents = processors.load_documents(location_directory / "docs.txt", split_by=split_by)

            # Perform the conversion to nlp format
            frame = processors.build_relation_extraction_nlp_data(documents, annotations, labels)

            # Finally add some sensible split labels that may or may not be adhered to
            frame = processors.split_train_test_val(frame)

            # Save
            frame.to_csv(self.processed_location / "{}.csv".format(location.split("/")[-1]))

        self.LOGGER.info("Processing successful.")
