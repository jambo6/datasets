__version__ = "0.1.0"

# Downloaders
from .biobert.biobert import BiobertDownloader
from .disgenet.disgenet import DisgenetDownloader
from .download import download
from .renet2.renet2 import RenetDownloader

# Dict of downloaders
DATASETS = {"renet2": RenetDownloader, "biobert": BiobertDownloader, "disgenet": DisgenetDownloader}

__all__ = ["download"]
