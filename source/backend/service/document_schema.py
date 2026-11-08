"""Schema of the documents table shared by the sources and the services."""

from enum import StrEnum


class DocumentColumn(StrEnum):
    """
    Columns of the documents table.
    Author: Corentin Legrand
    """

    TITLE = "title"
    AUTHOR = "author"
    DATE = "date"
    URL = "url"
    TEXT = "text"
    ORIGIN = "origin"
    NB_COMMENTS = "nb_comments"
    CO_AUTHORS = "co_authors"
