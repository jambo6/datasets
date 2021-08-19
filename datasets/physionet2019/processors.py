import os
import pathlib

import numpy as np
import pandas as pd
from tqdm import tqdm


def load_to_dataframe(download_location: pathlib.Path) -> pd.DataFrame:
    """Converts the raw psv files into a single dataframe with the hospital being marked.

    Args:
        download_location: The location where `training_setA` and `training_setB` directories are located.

    Returns:
        A pandas dataframe with the usual columns including SepsisLabel, hospital, and time.
    """
    # File locations
    locations = [download_location / x for x in ["training_setA", "training_setB"]]

    # Create a dataframe that notes the hospital (i.e. training set) that it came from
    data = []
    id = 0
    hospital = 1
    for loc in tqdm(locations):
        srt_dir = sorted(os.listdir(loc))
        for file in tqdm(srt_dir):
            id_df = pd.read_csv(loc / file, sep="|")
            id_df["id"] = id  # Give a unique id
            id_df["hospital"] = hospital  # Note the hospital
            data.append(id_df)
            id += 1
        hospital += 1

    # Concatenate into a full dataframe
    frame = pd.concat(data)
    frame.drop("Unnamed: 0", axis=1, errors="ignore", inplace=True)

    # Sort index and reorder columns
    frame.reset_index(inplace=True)
    frame.rename(columns={"index": "time"}, inplace=True)
    frame = frame[
        ["id", "time"] + [x for x in frame.columns if x not in ["id", "time", "SepsisLabel"]] + ["SepsisLabel"]
    ]
    frame.rename(columns={"SepsisLabel": "label"}, inplace=True)

    # Not needed when we have time
    frame.drop("ICULOS", axis=1, inplace=True)

    return frame


def convert_to_numpy_format(frame: pd.DataFrame) -> tuple[list[np.ndarray], list[np.ndarray], list[str]]:
    """Convert the data to numpy format. Outputs lists of data and a list of labels."""
    data, labels = [], []
    ids = frame["id"].unique()
    for id_ in tqdm(ids):
        subframe = frame[frame["id"] == id_].drop("id", axis=1)
        id_data = subframe.drop("label", axis=1)
        id_labels = subframe["label"]
        data.append(id_data.values)
        labels.append(id_labels.values)
    data_columns = id_data.columns
    return data, labels, data_columns
