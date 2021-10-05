import json
import os
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Any, Optional, Union

from loguru import logger


def make_directory_if_not_exists(path: Union[Path, str]) -> None:
    """Makes a directory at a specific location if one is not specified."""
    if not os.path.isdir(path):
        os.mkdir(path)


def read_text_file(filename: str) -> str:
    """Read a text file into a string"""
    with open(filename) as file:
        output = file.read()
    return output


def untar(tarname: Union[Path, str], extract_directory: Union[Path, str]) -> None:
    """Untar a filename to a specified location."""
    tar = tarfile.open(tarname)
    tar.extractall(extract_directory)


def unzip(zipname: Union[Path, str], extract_directory: Union[Path, str]) -> None:
    """Unzip a filename to a specified location."""
    with zipfile.ZipFile(zipname, "r") as zfile:
        zfile.extractall(extract_directory)


def load_json(filename: Union[Path, str]) -> dict[Any, Any]:
    """Simple json -> dict loader."""
    with open(filename, "rb") as file:
        return json.load(file)


def this_directory(file: str) -> Path:
    """Simply returns the directory in path object if presented with __file__."""
    return Path(file).parent


def get_logger(logfile: Optional[Union[Path, str]] = None) -> logger:
    """Returns a loguru logger."""
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    if logfile:
        logger.add(logfile)
    return logger
