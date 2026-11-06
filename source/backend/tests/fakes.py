"""Test doubles shared by the tests."""

from datetime import datetime, timezone

import pandas as pd

from service.document_schema import DocumentColumn
from service.interfaces.i_dao import IDAO


class InMemoryDAO(IDAO):
    """
    DAO keeping the documents table in memory.

    Attributes:
        content (pd.DataFrame): The stored table.

    Author: Corentin Legrand
    """

    def __init__(self, content: pd.DataFrame) -> None:
        """Build the DAO on a table.

        Args:
            content (pd.DataFrame): The stored table.
        """
        self.content: pd.DataFrame = content

    def create_data(self, content: pd.DataFrame, filename: str) -> None:
        """Replace the stored table.

        Args:
            content (pd.DataFrame): The table to store.
            filename (str): Ignored.
        """
        self.content = content

    def read_data(self, filename: str) -> pd.DataFrame:
        """Return the stored table.

        Args:
            filename (str): Ignored.

        Returns:
            pd.DataFrame: The stored table.
        """
        return self.content


def build_documents_table(texts: list[str]) -> pd.DataFrame:
    """Build a table of Reddit documents having the given texts.

    Args:
        texts (list[str]): The texts of the documents.

    Returns:
        pd.DataFrame: The documents table.
    """
    rows: list[dict[str, object]] = [
        {
            DocumentColumn.TITLE: f"title {index}",
            DocumentColumn.AUTHOR: "author",
            DocumentColumn.DATE: datetime(2026, 1, 1, tzinfo=timezone.utc),
            DocumentColumn.URL: f"https://example.com/{index}",
            DocumentColumn.TEXT: text,
            DocumentColumn.ORIGIN: "reddit",
            DocumentColumn.NB_COMMENTS: 0,
        }
        for index, text in enumerate(texts)
    ]
    return pd.DataFrame(rows)
