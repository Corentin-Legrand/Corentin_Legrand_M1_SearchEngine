"""Contract for persisting tabular data."""

from abc import ABC, abstractmethod

import pandas as pd


class IDAO(ABC):
    """
    Interface for data access objects storing and loading DataFrames.
    Author: Corentin Legrand
    """

    @abstractmethod
    def create_data(self, content: pd.DataFrame, filename: str) -> None:
        """Store a DataFrame.

        Args:
            content (pd.DataFrame): The data to store.
            filename (str): The name of the file holding the data.
        """

    @abstractmethod
    def read_data(self, filename: str) -> pd.DataFrame:
        """Load a DataFrame.

        Args:
            filename (str): The name of the file holding the data.

        Returns:
            pd.DataFrame: The stored data.
        """
