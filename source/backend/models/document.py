"""Base structure of a document of the corpus."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from models.document_origin import DocumentOrigin

if TYPE_CHECKING:
    from models.author import Author


@dataclass
class Document(ABC):
    """
    Document of the corpus, specialised by source.

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

    @property
    @abstractmethod
    def type(self) -> DocumentOrigin:
        """DocumentOrigin: The source the document comes from."""

    def __str__(self) -> str:
        """Return a digest of the document.

        Returns:
            str: The source and the title of the document.
        """
        return f"[{self.type}] {self.title}"
