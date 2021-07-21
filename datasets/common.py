import json
import os
import sys
import tarfile
from pathlib import Path
from typing import Any, Union

from loguru import logger


def make_directory_if_not_exists(path: Union[Path, str]) -> None:
    """Makes a directory at a specific location if one is not specified."""
    if not os.path.isdir(path):
        os.mkdir(path)


def untar(tarname: Union[Path, str], download_location: Union[Path, str]) -> None:
    """Untar a filename to a specified location."""
    tar = tarfile.open(tarname)
    tar.extractall(download_location)


def load_json(filename: Union[Path, str]) -> dict[Any, Any]:
    """Simple json -> dict loader."""
    with open(filename, "rb") as file:
        return json.load(file)


def this_directory(file: str) -> Path:
    """Simply returns the directory in path object if presented with __file__."""
    return Path(file).parent


def get_logger(logfile: Union[Path, str]) -> logger:
    """Returns a loguru logger."""
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(logfile)
    return logger
