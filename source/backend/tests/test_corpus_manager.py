"""Tests of the regular expression searches of the corpus manager."""

from collections.abc import Iterator
from datetime import datetime, timezone

import pandas as pd
import pytest

from helpers.regex_manager import ConcordanceColumn
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory
from service.document_schema import DocumentColumn
from service.interfaces.i_dao import IDAO

DATA_FILENAME: str = "test.json"
CONTEXT_SIZE: int = 5


class InMemoryDAO(IDAO):
    """
    DAO keeping the documents table in memory.

    Attributes:
        content (pd.DataFrame): The stored table.

    Author: Corentin Legrand
    """

    def __init__(self, content: pd.DataFrame) -> None:
        """Build the DAO on a table.

        Args:
            content (pd.DataFrame): The stored table.
        """
        self.content: pd.DataFrame = content

    def create_data(self, content: pd.DataFrame, filename: str) -> None:
        """Replace the stored table.

        Args:
            content (pd.DataFrame): The table to store.
            filename (str): Ignored.
        """
        self.content = content

    def read_data(self, filename: str) -> pd.DataFrame:
        """Return the stored table.

        Args:
            filename (str): Ignored.

        Returns:
            pd.DataFrame: The stored table.
        """
        return self.content


def build_documents_table(texts: list[str]) -> pd.DataFrame:
    """Build a table of Reddit documents having the given texts.

    Args:
        texts (list[str]): The texts of the documents.

    Returns:
        pd.DataFrame: The documents table.
    """
    rows: list[dict[str, object]] = [
        {
            DocumentColumn.TITLE: f"title {index}",
            DocumentColumn.AUTHOR: "author",
            DocumentColumn.DATE: datetime(2026, 1, 1, tzinfo=timezone.utc),
            DocumentColumn.URL: f"https://example.com/{index}",
            DocumentColumn.TEXT: text,
            DocumentColumn.ORIGIN: "reddit",
            DocumentColumn.NB_COMMENTS: 0,
        }
        for index, text in enumerate(texts)
    ]
    return pd.DataFrame(rows)


@pytest.fixture
def dao() -> InMemoryDAO:
    """Return a DAO holding two documents."""
    return InMemoryDAO(build_documents_table(["Solar energy is clean. It is cheap.", "Wind energy is variable."]))


@pytest.fixture
def corpus_manager(dao: InMemoryDAO) -> Iterator[CorpusManager]:
    """Return a manager whose corpus is loaded from the DAO, and empty the corpus afterwards."""
    manager: CorpusManager = CorpusManager(dao, CorpusMapper(DocumentFactory(), AuthorManager()), DATA_FILENAME)
    manager.load()
    yield manager
    manager.clear_corpus()


def test_search_returns_passages_of_every_document(corpus_manager: CorpusManager) -> None:
    """The passages come from all the documents of the corpus."""
    assert corpus_manager.search("energy") == ["Solar energy is clean", "Wind energy is variable"]


def test_concorde_returns_one_row_per_occurrence(corpus_manager: CorpusManager) -> None:
    """Each occurrence in the corpus gives one row."""
    assert len(corpus_manager.concorde(r"\bis\b", CONTEXT_SIZE)) == 3


def test_concorde_keeps_context_within_document(corpus_manager: CorpusManager) -> None:
    """The right context of the last word of a document stops at the document end."""
    concordances: pd.DataFrame = corpus_manager.concorde("cheap", CONTEXT_SIZE)
    assert concordances.iloc[0][ConcordanceColumn.RIGHT_CONTEXT] == "."


def test_search_cache_is_reset_on_load(corpus_manager: CorpusManager, dao: InMemoryDAO) -> None:
    """After a new load, the searches use the new documents and not the cached text."""
    corpus_manager.search("energy")
    dao.content = build_documents_table(["Nuclear energy is stable."])
    corpus_manager.load()
    assert corpus_manager.search("energy") == ["Nuclear energy is stable"]
