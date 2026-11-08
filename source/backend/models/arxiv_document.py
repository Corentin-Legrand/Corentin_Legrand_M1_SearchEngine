"""Document coming from Arxiv."""

from dataclasses import dataclass

from models.document import Document
from models.document_origin import DocumentOrigin


@dataclass
class ArxivDocument(Document):
    """
    Arxiv article.

    Attributes:
        co_authors (list[str]): Names of the authors other than the main one.

    Author: Corentin Legrand
    """

    co_authors: list[str]

    @property
    def type(self) -> DocumentOrigin:
        """DocumentOrigin: Always `DocumentOrigin.ARXIV`."""
        return DocumentOrigin.ARXIV
