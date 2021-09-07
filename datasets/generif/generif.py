# """
# A utility script for downloading data from the Harmonizome, with the ability to configure which datasets and which
# download types from which to download. Note that all content decompressed is roughly 30GB. The default is to not
# decompress the files on download.
# """
# import subprocess
# import pandas as pd
# import wget
# from datasets import common
# from datasets.base import DownloadBase
#
# logger = common.get_logger()
#
#
# class GeneRIFDownloader(DownloadBase):
#     """Downloader class for the DisGeNET data."""
#
#     DATASET_NAME = "geneRIF"
#     MODULE_DIR = common.this_directory(__file__)
#     DOWNLOAD_URL = "https://ftp.ncbi.nih.gov/gene/GeneRIF/"
#     DOWNLOAD_APPEND = ['interactions.gz', 'generifs_basic.gz', 'interaction_sources']
#     LOGGER = logger
#
#     def _download(self) -> None:
#         self.LOGGER.info("Downloading the {} database".format(self.DATASET_NAME))
#         for append_name in self.DOWNLOAD_APPEND:
#             outfile = self.download_location / append_name
#             wget.download("{}/{}".format(self.DOWNLOAD_URL, append_name), str(outfile))
#             #
#             self.LOGGER.info("Unzipping")
#             # subprocess.call("gunzip {}".format(outfile))
#
#     def _process(self) -> None:
#         interactions = pd.read_csv(self.download_location / "interactions", sep='\t', low_memory=False)
#         generifs = pd.read_csv(self.download_location / "generifs_basic", sep='\t', low_memory=False)
#         pass
#
#
# if __name__ == '__main__':
#     GeneRIFDownloader("../../data/geneRIF").process()
