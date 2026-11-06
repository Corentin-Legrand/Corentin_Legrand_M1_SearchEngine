"""Tests of the regular expression searches of the corpus manager."""

from collections.abc import Iterator

import pandas as pd
import pytest

from helpers.regex_manager import ConcordanceColumn
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory
from tests.fakes import InMemoryDAO, build_documents_table

DATA_FILENAME: str = "test.json"
CONTEXT_SIZE: int = 5


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
