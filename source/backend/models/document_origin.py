"""Sources a document can come from."""

from enum import StrEnum


class DocumentOrigin(StrEnum):
    """
    Sources the documents come from.
    Author: Corentin Legrand
    """

    REDDIT = "reddit"
    ARXIV = "arxiv"
