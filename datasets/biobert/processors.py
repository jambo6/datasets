"""Biobert processing funcitons.

So far we are only considering the relation extraction tasks for GAD and EUADR.

We convert tsvs -> csvs and merge the train and test sets into the same file.
"""
from pathlib import Path

import pandas as pd

from datasets import common

logger = common.get_logger(common.this_directory(__file__) / "logfile.log")


def open_re(folder: Path) -> pd.DataFrame:
    """Open the GAD data into a standardised format."""
    train = pd.read_csv(folder / "train.tsv", sep="\t", header=None)
    test = pd.read_csv(folder / "test.tsv", sep="\t", index_col=0)
    train.columns = test.columns
    frame = pd.concat([train, test])
    frame = frame.sort_values("sentence").reset_index().drop("index", axis=1)
    return frame


def process_re(download_location: Path, processed_location: Path) -> None:
    """Processes both RE datasets."""
    datasets = ["GAD", "euadr"]
    for dataset in datasets:
        logger.info("{} processing started...".format(dataset))
        frame = open_re(download_location / dataset / "1")
        frame.to_csv(processed_location / "{}.csv".format(dataset))
        logger.info("{} completed successfully.".format(dataset))


def split_train_test_val() -> None:
    """Build a method that can sort sentences into groups even with tokenized gene and disease names."""
    pass
