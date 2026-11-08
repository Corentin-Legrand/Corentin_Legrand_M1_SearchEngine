"""Contract for reading tabular data from JSON files."""

from abc import ABC, abstractmethod

import pandas as pd


class IJsonReader(ABC):
    """
    Interface for components reading a JSON file into a DataFrame.
    Author: Corentin Legrand
    """

    @abstractmethod
    def read_json(self, filename: str) -> pd.DataFrame:
        """Read a JSON file into a DataFrame.

        Args:
            filename (str): The name of the file to read (e.g. `corpus.json`).

        Returns:
            pd.DataFrame: The data contained in the file.
        """
