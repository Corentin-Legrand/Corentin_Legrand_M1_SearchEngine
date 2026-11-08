"""Statistics about an author."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorStats:
    """
    Statistics computed on the production of an author.

    Attributes:
        nb_document (int): Number of documents written by the author.
        average_size (int): Average number of characters of these documents.

    Author: Corentin Legrand
    """

    nb_document: int
    average_size: int
