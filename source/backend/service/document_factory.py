"""Factory creating the right kind of document from a document row."""

import pandas as pd

from models.document import Document
from models.document_origin import DocumentOrigin
from service.arxiv_document_builder import ArxivDocumentBuilder
from service.document_schema import DocumentColumn
from service.reddit_document_builder import RedditDocumentBuilder


class UnknownDocumentOriginError(ValueError):
    """
    Raised when a document row comes from an unsupported source.
    Author: Corentin Legrand
    """


class DocumentFactory:
    """
    Create the document matching the origin of a row.

    Attributes:
        reddit_builder (RedditDocumentBuilder): Builder of Reddit documents (private).
        arxiv_builder (ArxivDocumentBuilder): Builder of Arxiv documents (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the factory and its builders."""
        self.__reddit_builder: RedditDocumentBuilder = RedditDocumentBuilder()
        self.__arxiv_builder: ArxivDocumentBuilder = ArxivDocumentBuilder()

    def create_document(self, row: pd.Series) -> Document:
        """Create the document described by a row.

        Args:
            row (pd.Series): The document row, with `DocumentColumn` columns.

        Returns:
            Document: A `RedditDocument` or an `ArxivDocument`, according to the row origin.

        Raises:
            UnknownDocumentOriginError: If the origin of the row is not a `DocumentOrigin`.
        """
        document: Document
        match self.__get_origin(row):
            case DocumentOrigin.REDDIT:
                document = self.__reddit_builder.create_reddit_document(row)
            case DocumentOrigin.ARXIV:
                document = self.__arxiv_builder.create_arxiv_document(row)
        return document

    @staticmethod
    def __get_origin(row: pd.Series) -> DocumentOrigin:
        """Read the origin of a row.

        Args:
            row (pd.Series): The document row.

        Returns:
            DocumentOrigin: The source of the document.

        Raises:
            UnknownDocumentOriginError: If the origin of the row is not a `DocumentOrigin`.
        """
        origin: str = str(row[DocumentColumn.ORIGIN])
        try:
            return DocumentOrigin(origin)
        except ValueError as error:
            raise UnknownDocumentOriginError(f"Unknown document origin '{origin}'.") from error
