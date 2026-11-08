"""Schema of the tables produced by the textual analysis of the corpus."""

from enum import StrEnum


class FrequencyColumn(StrEnum):
    """
    Columns of the word frequencies table.
    Author: Corentin Legrand
    """

    WORD = "word"
    TERM_FREQUENCY = "term_frequency"
    DOCUMENT_FREQUENCY = "document_frequency"


class SearchResultColumn(StrEnum):
    """
    Columns of the search results table.
    Author: Corentin Legrand
    """

    SCORE = "score"
    DOCUMENT_ID = "document_id"
    TITLE = "title"
    AUTHOR = "author"
    DATE = "date"
    ORIGIN = "origin"
    URL = "url"
