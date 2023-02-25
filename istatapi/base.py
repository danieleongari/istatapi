# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_base.ipynb.

# %% auto 0
__all__ = ['ISTAT']

# %% ../nbs/00_base.ipynb 1
import requests
from nbdev.showdoc import show_doc
from importlib import reload

# %% ../nbs/00_base.ipynb 2
class ISTAT:
    """Base class that provides useful functions to communicate with ISTAT API"""

    def __init__(self):
        self.base_url = "http://sdmx.istat.it/SDMXWS/rest"
        self.agencyID = "IT1"

    def _request(self, path, **kwargs):
        """Make a request to ISTAT API given a 'path'"""
        url = "/".join([self.base_url, path])

        if "headers" in kwargs.keys():
            response = requests.get(url, headers=kwargs["headers"])
        else:
            response = requests.get(url)

        return response

# %% ../nbs/00_base.ipynb 3
class ISTAT:
    """Base class that provides useful functions to communicate with ISTAT API"""

    def __init__(self):
        self.base_url = "http://sdmx.istat.it/SDMXWS/rest"
        self.agencyID = "IT1"

    def _request(self, path, **kwargs):
        """Make a request to ISTAT API given a 'path'"""
        url = "/".join([self.base_url, path])

        if "headers" in kwargs.keys():
            response = requests.get(url, headers=kwargs["headers"])
        else:
            response = requests.get(url)

        return response
