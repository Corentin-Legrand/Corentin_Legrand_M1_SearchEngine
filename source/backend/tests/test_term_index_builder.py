"""Tests of the Documents x Terms matrices, on the example of the course."""

from collections.abc import Callable

import numpy as np
import pytest

from models.corpus import Corpus
from models.term_index import TermIndex
from models.vocabulary_entry import VocabularyEntry
from service.term_index_builder import TermIndexBuilder

# Example of the course: 3 documents described by {carbon, climate, energy, solar}.
COURSE_TEXTS: list[str] = ["Solar energy, solar!", "carbon energy", "Carbon climate"]
IDF_RARE_WORD: float = float(np.log(3 / 1))
IDF_COMMON_WORD: float = float(np.log(3 / 2))


@pytest.fixture
def index(load_corpus: Callable[[list[str]], Corpus]) -> TermIndex:
    """Return the index of the course example."""
    return TermIndexBuilder().build(load_corpus(COURSE_TEXTS))


def test_vocab_is_sorted_alphabetically(index: TermIndex) -> None:
    """The words are cleaned, deduplicated and sorted."""
    assert list(index.vocab) == ["carbon", "climate", "energy", "solar"]


def test_vocab_identifier_is_alphabetical_position(index: TermIndex) -> None:
    """The id of a word is its position, i.e. its matrix column."""
    assert [entry.identifier for entry in index.vocab.values()] == [0, 1, 2, 3]


def test_vocab_counts_occurrences_and_documents(index: TermIndex) -> None:
    """"solar" occurs twice, in a single document."""
    assert index.vocab["solar"] == VocabularyEntry(identifier=3, nb_occurrences=2, nb_documents=1)


def test_document_frequency_differs_from_term_frequency(index: TermIndex) -> None:
    """"energy" occurs once in each of two documents."""
    assert (index.vocab["energy"].nb_occurrences, index.vocab["energy"].nb_documents) == (2, 2)


def test_tf_matrix_has_one_row_per_document_and_one_column_per_word(index: TermIndex) -> None:
    """The matrix shape is (number of documents) x (size of the vocabulary)."""
    assert index.mat_tf.shape == (3, 4)


def test_tf_matrix_holds_occurrences(index: TermIndex) -> None:
    """Cell (i, j) is the number of occurrences of word j in document i."""
    assert index.mat_tf.toarray().tolist() == [[0, 0, 1, 2], [1, 0, 1, 0], [1, 1, 0, 0]]


def test_document_ids_match_matrix_rows(index: TermIndex) -> None:
    """Row i of the matrices describes the document `document_ids[i]`."""
    assert index.document_ids == [0, 1, 2]


def test_idf_rewards_rare_words(index: TermIndex) -> None:
    """idf = log(N / df), as in the course (0.41 for a word in 2 of 3 documents, 1.10 for 1 of 3)."""
    expected: list[float] = [IDF_COMMON_WORD, IDF_RARE_WORD, IDF_COMMON_WORD, IDF_RARE_WORD]
    assert index.idf == pytest.approx(expected)


def test_tfidf_matrix_multiplies_tf_by_idf(index: TermIndex) -> None:
    """Cell (i, j) is tf(j, i) x idf(j): document 1 is carried by "solar" (2 x 1.10)."""
    expected: list[float] = [0.0, 0.0, IDF_COMMON_WORD, 2 * IDF_RARE_WORD]
    assert index.mat_tfidf.toarray()[0] == pytest.approx(expected)


def test_word_present_everywhere_has_null_tfidf(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """A word present in all the documents does not discriminate them."""
    index: TermIndex = TermIndexBuilder().build(load_corpus(["the sun", "the wind"]))
    assert index.mat_tfidf.toarray()[:, index.vocab["the"].identifier] == pytest.approx([0.0, 0.0])


def test_empty_corpus_gives_empty_index(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """An empty corpus has neither documents nor words."""
    assert TermIndexBuilder().build(load_corpus([])).mat_tfidf.shape == (0, 0)
