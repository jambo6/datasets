import pandas as pd
import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class Snorkeling(DownloadBase):
    """Downloader class for the Snorkeling database.

    Snorkeling has a few categories, including compounds and disease ones. However, its a bit unclear what is going on.
    """

    DATASET_NAME = "Snorkeling"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = (
        "https://github.com/greenelab/snorkeling/blob/master/disease_gene/disease_associates_gene/data/sentences/"
    )
    LOGGER = logger

    def _download(self) -> None:
        self.LOGGER.info("Downloading the {} database...".format(self.DATASET_NAME))
        for excel_file in ["sentence_labels_dev.xlsx", "sentence_labels_test.xlsx"]:
            outfile = self.download_location / "{}".format(excel_file)
            wget.download("{}/{}".format(self.DOWNLOAD_URL, excel_file), out=str(outfile))

    def _process(self) -> None:
        # Load all
        frames = [
            pd.read_excel(self.download_location / "sentence_labels_{}.xlsx".format(name)) for name in ("dev", "test")
        ]
        frame = pd.concat(frames)

        # Todo: Find out what dsh, ctg, cug and all that means.

        def rewrite_sentences(row: pd.DataFrame) -> pd.DataFrame:
            sentence = row['sentence']
            gene, disease = row['gene'], row['disease']
            for x in gene, disease:
                sentence.replace("~~{}~~".format(x), "")

        frame = frame.apply(rewrite_sentences, axis=1)


if __name__ == "__main__":
    Snorkeling(download_location="../../data/snorkeling").process()
