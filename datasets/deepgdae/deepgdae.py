import os

import pandas as pd
import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class DeepGdaeDownloader(DownloadBase):
    """Downloader class for the BC5DR data."""

    DATASET_NAME = "DeepGDAE"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/gj7nvvktk6-1.zip"
    LOGGER = logger

    def _download(self) -> None:
        self.LOGGER.info("Downloading the {} database...".format(self.DATASET_NAME))
        outfile = self.download_location / "gdae_data.zip"
        wget.download(self.DOWNLOAD_URL, str(outfile))

        common.unzip(outfile, self.download_location)

    def _process_snp_data(self) -> None:
        """Processes the SNP data to a standard format csv."""
        frames = []
        for split in ("train", "test"):
            f = pd.read_csv(self.data_folder / "SNP_{}_data.txt".format(split), sep="\t")
            f["split"] = split
            frames.append(f)
        frame = pd.concat(frames)
        frame.rename(columns={"sentence": "doc", "lable": "label"}, inplace=True)

        def tokenize(row: pd.DataFrame) -> pd.DataFrame:
            row["snp"] = row["snp"].replace("\xa0", " ")
            row["phenotype"] = row["phenotype"].replace("\xa0", " ")
            row["doc"] = row["doc"].replace(row["snp"], "@SNP$")
            row["doc"] = row["doc"].replace(row["phenotype"], "@PHENOTYPE$")
            if not all([x in row["doc"] for x in ("@SNP$", "@PHENOTYPE$")]):
                logger.warning("Error with \n\tSNP: {}\n\tPhenotype: {}".format(row["snp"], row["phenotype"]))
            while "  " in row["doc"]:
                row["doc"] = row["doc"].replace("  ", " ")
            return row

        frame = frame.apply(tokenize, axis=1)
        frame = frame.reset_index().drop("index", axis=1)
        frame.to_csv(self.download_location / "processed" / "snp_data.csv")

    def _process_gad_data(self) -> None:
        """GAD data still looks low-quality, so I may not use it"""
        frames = []
        files = os.listdir(self.data_folder / "our_corpus")
        for split in ("train", "val", "test"):
            file = [x for x in files if x.startswith(split)][0]
            f = pd.read_csv(self.data_folder / "our_corpus" / file)
            f["split"] = split
            frames.append(f)
        frame = pd.concat(frames)

        # Binarize and drop therapeutic label
        frame["label"] = frame["associationType"].replace(("Negative", "Biomarker", "Therapeutic"), (0, 1, 2))
        frame = frame[~(frame["label"] == 2)]

        def tokenize(row: pd.DataFrame) -> pd.DataFrame:
            s = row["raw_sentence"]
            s = s.replace(row["gene_mention"], "@GENE$")
            s = s.replace(row["disease_mention"], "@DISEASE$")
            row["raw_sentence"] = s
            return row

        frame = frame.apply(tokenize, axis=1)
        frame.rename(columns={"raw_sentence": "doc"}, inplace=True)
        frame = frame[["pmid", "doc", "label", "split"]]
        frame = frame.reset_index().drop("index", axis=1)
        frame.to_csv(self.download_location / "processed" / "gad_data.csv")

    def _process(self) -> None:
        # Init
        common.make_directory_if_not_exists(self.download_location / "processed")
        self.data_folder = self.download_location / "Deep-GDAE-master" / "data"

        # SNP data
        if not os.path.isfile(self.download_location / "processed" / "snp_data.csv"):
            self._process_snp_data()
        else:
            logger.info("SNP data already exists, skipping.")

        if not os.path.isfile(self.download_location / "processed" / "gad_data.csv"):
            self._process_gad_data()
        else:
            logger.info("GAD data already exists, skipping.")
