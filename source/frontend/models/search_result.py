"""A document found by the search engine."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SearchResult:
    """
    A document found by a search, as returned by the search API.

    Attributes:
        score (float): Cosine similarity between the document and the query.
        document_id (int): Identifier of the document in the corpus.
        title (str): Title of the document.
        author (str): Name of the author of the document.
        date (datetime): Publication date of the document.
        origin (str): Source of the document (`reddit` or `arxiv`).
        url (str): Address of the document.

    Author: Corentin Legrand
    """

    score: float
    document_id: int
    title: str
    author: str
    date: datetime
    origin: str
    url: str
