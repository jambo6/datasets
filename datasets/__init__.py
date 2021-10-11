__version__ = "0.1.0"

# Downloaders
from .bc5cdr.bc5dr import Bc5drDownloader
from .biobert.biobert import BiobertDownloader
from .deepgdae.deepgdae import DeepGdaeDownloader
from .disgenet.disgenet import DisgenetDownloader
from .download import download
from .renet2.renet2 import RenetDownloader

# Dict of downloaders
DATASETS = {
    "bc5dr": Bc5drDownloader,
    "biobert": BiobertDownloader,
    "deepgdae": DeepGdaeDownloader,
    "disgenet": DisgenetDownloader,
    "renet2": RenetDownloader,
}

__all__ = ["download"]
