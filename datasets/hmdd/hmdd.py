from typing import Optional

import pandas as pd
import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class HmddDownloader(DownloadBase):
    """Downloader class for the HMDD database.

    The processing logic is relatively simple so it is all enclosed within this classes process function. The only
    tricky aspect with this download is that the data is spread over multiple files. For this reason, we have opted for
    a slightly unconventional approach with a `DOWNLOAD_URL_APPEND` list that contains the ends of all the files to be
    included after `DOWNLOAD_URL`.
    """

    DATASET_NAME = "HMDD"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "https://www.cuilab.cn/static/hmdd3/data/"  # This is the base URL
    CAUSALITY_URL = "https://www.cuilab.cn/static/hmdd3/data/hmdd3.2_causality.txt"
    LOGGER = logger

    DOWNLOAD_URL_APPEND = [
        "alldata.xlsx",
        "S1_HMDD3_causal_info.xlsx",
        "S2_miRNA_conservation_info.xlsx",
        "v3_alldata.txt",
    ]

    def _download(self) -> None:
        self.LOGGER.info("Downloading the HMDD database...")
        for dl_append in self.DOWNLOAD_URL_APPEND:
            outfile = self.download_location / "{}".format(dl_append)
            loc = "{}/{}".format(self.DOWNLOAD_URL, dl_append)
            wget.download(loc, str(outfile))

    def _process(self) -> None:
        # Main processing component
        frame = pd.read_excel(self.download_location / "alldata.xlsx")
        causality_frame = pd.read_excel(self.download_location / "S1_HMDD3_causal_info.xlsx")

        # Fix two small naming discrepancies
        frame = frame.replace("hepatocellular carcinoma", "Carcinoma, Hepatocellular")
        causality_frame = causality_frame.replace("hsa-mir-200C", "hsa-mir-200c")
        assert (frame[["mir", "disease"]].values != causality_frame[["mir", "disease"]].values).sum() == 0

        # Now add causalities to main frame
        frame["causality"] = causality_frame["causality"]
        frame["mesh_name"] = causality_frame["mesh_name"]

        # Now sort the
        overview_frame = pd.read_excel(self.download_location / "S2_miRNA_conservation_info.xlsx", header=1)

        # Finally attempt to add mesh ids from the alldata file
        mesh_frame = pd.read_csv(self.download_location / "v3_alldata.txt", sep="\t", usecols=["disease", "mesh"])
        disease_to_mesh = mesh_frame.drop_duplicates().set_index("disease")["mesh"]

        def find_mesh(s: str) -> Optional[str]:
            if s in disease_to_mesh.index:
                return disease_to_mesh.loc[s]
            return None

        frame["mesh"] = frame["disease"].apply(find_mesh)

        # Saves
        frame.to_csv(self.processed_location / "alldata.csv")
        overview_frame.to_csv(self.processed_location / "overview.csv")
