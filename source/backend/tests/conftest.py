"""Fixtures shared by the tests."""

from collections.abc import Callable, Iterator

import pytest

from models.corpus import Corpus
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory
from tests.fakes import InMemoryDAO, build_documents_table

DATA_FILENAME: str = "test.json"


@pytest.fixture
def load_corpus() -> Iterator[Callable[[list[str]], Corpus]]:
    """Return a function filling the unique corpus with documents of given texts, emptied afterwards."""
    dao: InMemoryDAO = InMemoryDAO(build_documents_table([]))
    corpus_manager: CorpusManager = CorpusManager(dao, CorpusMapper(DocumentFactory(), AuthorManager()), DATA_FILENAME)

    def load(texts: list[str]) -> Corpus:
        dao.content = build_documents_table(texts)
        corpus_manager.load()
        return Corpus.get_instance()

    yield load
    corpus_manager.clear_corpus()
