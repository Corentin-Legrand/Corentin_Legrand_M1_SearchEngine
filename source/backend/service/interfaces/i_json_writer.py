"""Contract for writing tabular data to JSON files."""

from abc import ABC, abstractmethod

import pandas as pd


class IJsonWriter(ABC):
    """
    Interface for components writing a DataFrame to a JSON file.
    Author: Corentin Legrand
    """

    @abstractmethod
    def write_to_json(self, content: pd.DataFrame, filename: str) -> None:
        """Write a DataFrame to a JSON file.

        Args:
            content (pd.DataFrame): The data to write.
            filename (str): The name of the file to write (e.g. `corpus.json`).
        """
