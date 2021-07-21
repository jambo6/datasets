__version__ = "0.1.0"

# Downloaders
from .renet2.renet2 import RenetDownloader

# from .biobert.biobert import BiobertDownloader

# Dict of downloaders
DATASETS = {
    "renet2": RenetDownloader,
    # "biobert": BiobertDownloader
}
