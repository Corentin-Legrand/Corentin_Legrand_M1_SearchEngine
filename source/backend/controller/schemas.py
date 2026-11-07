"""Data transfer objects exposed by the API."""

from datetime import datetime

from pydantic import BaseModel


class SearchResultDTO(BaseModel):
    """
    A document found by a search.

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


class ErrorDTO(BaseModel):
    """
    Description of a rejected request.

    Attributes:
        detail (str): Why the request was rejected.

    Author: Corentin Legrand
    """

    detail: str
