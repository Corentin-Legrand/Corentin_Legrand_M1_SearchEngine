"""Tests of the Okapi BM25 score."""

from collections.abc import Callable

import numpy as np
import pytest

from models.corpus import Corpus
from models.term_index import TermIndex
from service.bm25_similarity import Bm25Similarity
from service.term_index_builder import TermIndexBuilder

# Example of the course; with k1 = 1.2 and b = 0.75, "solar energy" gives D1 = 1.670, D2 = 0.499 and D3 = 0.
COURSE_TEXTS: list[str] = ["solar energy solar", "carbon energy", "carbon climate"]
COURSE_SCORES: list[float] = [1.670, 0.499, 0.0]
SCORE_TOLERANCE: float = 1e-3


def build_index(load_corpus: Callable[[list[str]], Corpus], texts: list[str]) -> TermIndex:
    """Index a corpus of the given texts.

    Args:
        load_corpus (Callable[[list[str]], Corpus]): Fixture filling the corpus.
        texts (list[str]): The texts of the documents.

    Returns:
        TermIndex: The index of the corpus.
    """
    return TermIndexBuilder().build(load_corpus(texts))


def count_query(index: TermIndex, counts: dict[str, int]) -> np.ndarray:
    """Build the occurrences vector of a query.

    Args:
        index (TermIndex): The index of the corpus.
        counts (dict[str, int]): The number of occurrences of each word of the query.

    Returns:
        np.ndarray: The number of occurrences of each word of the vocabulary in the query.
    """
    query_counts: np.ndarray = np.zeros(len(index.vocab))
    for word, count in counts.items():
        query_counts[index.vocab[word].identifier] = count
    return query_counts


def test_scores_of_course_example(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """The scores are the ones computed by hand on the course example."""
    index: TermIndex = build_index(load_corpus, COURSE_TEXTS)
    scores: np.ndarray = Bm25Similarity(index).compute_scores(count_query(index, {"solar": 1, "energy": 1}))
    assert scores.tolist() == pytest.approx(COURSE_SCORES, abs=SCORE_TOLERANCE)


def test_repeated_query_word_counts_once(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """Repeating a word in the query does not change the scores."""
    index: TermIndex = build_index(load_corpus, COURSE_TEXTS)
    similarity: Bm25Similarity = Bm25Similarity(index)
    repeated: np.ndarray = similarity.compute_scores(count_query(index, {"solar": 3}))
    assert repeated.tolist() == similarity.compute_scores(count_query(index, {"solar": 1})).tolist()


def test_longer_document_scores_lower(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """For the same number of occurrences, the longer document gets the lower score."""
    index: TermIndex = build_index(load_corpus, ["solar", "solar carbon climate energy", "carbon"])
    scores: np.ndarray = Bm25Similarity(index).compute_scores(count_query(index, {"solar": 1}))
    assert scores[0] > scores[1]


def test_term_frequency_saturates(load_corpus: Callable[[list[str]], Corpus]) -> None:
    """Without length normalisation, a word weight never exceeds IDF x (k1 + 1)."""
    index: TermIndex = build_index(load_corpus, [" ".join(["solar"] * 1000), "carbon"])
    similarity: Bm25Similarity = Bm25Similarity(index, k1=1.2, b=0.0)
    idf: float = float(np.log((2 - 1 + 0.5) / (1 + 0.5) + 1))
    assert similarity.compute_scores(count_query(index, {"solar": 1}))[0] < idf * 2.2
