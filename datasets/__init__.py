__version__ = "0.1.0"

# Downloaders
from .biobert.biobert import BiobertDownloader
from .download import download
from .renet2.renet2 import RenetDownloader

# Dict of downloaders
DATASETS = {"renet2": RenetDownloader, "biobert": BiobertDownloader}

__all__ = ["download"]
