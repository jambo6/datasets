import os
import subprocess
from copy import deepcopy

import pandas as pd
import wget

from datasets import common
from datasets.base import DownloadBase

logger = common.get_logger()


class Bc5drDownloader(DownloadBase):
    """Downloader class for the BC5DR data."""

    DATASET_NAME = "BC5DR"
    MODULE_DIR = common.this_directory(__file__)
    DOWNLOAD_URL = "http://www.biocreative.org/media/store/files/2016/CDR_Data.zip"
    LOGGER = logger

    def _download(self) -> None:
        # Type is gzip
        self.LOGGER.info("Downloading the {} database...".format(self.DATASET_NAME))
        outfile = self.download_location / "CDR_DATA.zip"
        wget.download(self.DOWNLOAD_URL, str(outfile))

        # Call gunzip
        self.LOGGER.info("Unzipping the database.")
        subprocess.call("gunzip {}".format(outfile))

        # Unzip then remove the zipfile
        os.remove(outfile)

    def _process(self) -> None:
        locations = [
            "CDR_DATA/CDR.Corpus.v010516/CDR_{}.PubTator.txt".format(x)
            for x in ("TrainingSet", "DevelopmentSet", "TestSet")
        ]
        names = ["train", "devel", "test"]

        # Will take the form (pmid, doc, label, split)
        processed_data = []
        for name, location in zip(names, locations):
            self.LOGGER.info("Processing {}...".format(location))

            file = self.download_location / location
            datas = common.read_text_file(str(file)).split("\n\n")
            if datas[-1] == "":
                datas = datas[:-1]
            for data in datas:
                # Load the data, which is currently all mushed together
                column_names = ["pmid", "start_idx", "end_idx", "mention", "type", "id"]
                # Simplify things by ignoring multi-definitions
                line_split = [x.split("\t") for x in data.split("\n")][:-1]
                line_split = [[x for x in y if x != ""] for y in line_split]
                line_split = [x for x in line_split if len(x) < 7]
                frame = pd.DataFrame(line_split, columns=column_names)

                # Split the abstract and pmid information from the top
                pmid = int(frame.iloc[0][0].split("|")[0])
                abstract = frame.iloc[0][0].split("|")[2] + " " + frame.iloc[1][0].split("|")[2]
                sub_frame = frame.iloc[2:]

                # Extract the label information. Gives the form (chemical, disease).
                label_info = sub_frame[sub_frame["start_idx"] == "CID"]
                positive_labels = [(row["end_idx"], row["mention"]) for _, row in label_info.iterrows()]

                # Concatenate the mentions
                mention_frame = sub_frame[sub_frame["start_idx"] != "CID"]
                cat_frame = mention_frame.groupby(["id", "type"])["mention"].apply(lambda x: "||".join(x)).reset_index()
                cat_frame = cat_frame[cat_frame["id"] != "-1"]

                # Tokenize the abstract and append the label
                for _, disease_row in cat_frame[cat_frame["type"] == "Disease"].iterrows():
                    abstract_tokenized = deepcopy(abstract)
                    disease_id = disease_row["id"]
                    disease_mentions = disease_row["mention"]
                    for m in disease_mentions.split("||"):
                        abstract_tokenized = abstract_tokenized.replace(m, "@DISEASE$")

                    for _, chem_row in cat_frame[cat_frame["type"] == "Chemical"].iterrows():
                        chem_id = chem_row["id"]
                        chem_mentions = chem_row["mention"]
                        for m in chem_mentions.split("||"):
                            abstract_tokenized = abstract_tokenized.replace(m, "@CHEMICAL$")

                        # Add the data
                        label = 1 if (chem_id, disease_id) in positive_labels else 0
                        data_to_add = [pmid, abstract_tokenized, label, name]
                        processed_data.append(data_to_add)

        # Save the processed data
        processed_frame = pd.DataFrame(processed_data, columns=["pmid", "doc", "label", "split"])
        processed_frame.to_csv(self.processed_location / "data.csv")

        self.LOGGER.info("Processing successful.")
