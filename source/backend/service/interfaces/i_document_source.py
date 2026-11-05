"""Contract for external sources of documents."""

from abc import ABC, abstractmethod

import pandas as pd


class IDocumentSource(ABC):
    """
    Interface for components fetching documents from an external source.
    Author: Corentin Legrand
    """

    @abstractmethod
    def fetch_documents(self, query: str, max_results: int) -> pd.DataFrame:
        """Fetch the documents matching a query.

        Args:
            query (str): The keywords to search.
            max_results (int): The maximum number of documents to fetch.

        Returns:
            pd.DataFrame: One row per document, with `DocumentColumn` columns.
        """
