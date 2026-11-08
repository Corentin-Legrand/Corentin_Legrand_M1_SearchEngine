"""Base of the builders turning a document row into a document."""

from datetime import datetime
from typing import TypedDict

import pandas as pd

from models.author import Author
from service.document_schema import DocumentColumn


class DocumentFields(TypedDict):
    """
    Fields shared by every kind of document.

    Attributes:
        title (str): Title of the document.
        author (Author): Main author of the document.
        date (datetime): Publication date.
        url (str): Source URL.
        text (str): Textual content.

    Author: Corentin Legrand
    """

    title: str
    author: Author
    date: datetime
    url: str
    text: str


class DocumentBuilder:
    """
    Base of the document builders, reading the fields shared by every source.
    Author: Corentin Legrand
    """

    def _build_common_fields(self, row: pd.Series) -> DocumentFields:
        """Read the fields shared by every kind of document from a row.

        The author is a new `Author`; `AuthorManager` replaces it by the corpus' one.

        Args:
            row (pd.Series): The document row, with `DocumentColumn` columns.

        Returns:
            DocumentFields: The shared fields, ready to be passed to a document constructor.
        """
        return DocumentFields(
            title=str(row[DocumentColumn.TITLE]),
            author=Author(str(row[DocumentColumn.AUTHOR])),
            date=pd.Timestamp(row[DocumentColumn.DATE]).to_pydatetime(),
            url=str(row[DocumentColumn.URL]),
            text=str(row[DocumentColumn.TEXT]),
        )
