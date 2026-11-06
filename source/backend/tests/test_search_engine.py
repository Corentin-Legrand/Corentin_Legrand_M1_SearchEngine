"""Tests of the search engine: word statistics and search."""

from collections.abc import Callable

import pandas as pd
import pytest

from models.corpus import Corpus
from service.search_engine import EmptyQueryError, InvalidNbDocumentsError, SearchEngine
from service.text_analysis_schema import FrequencyColumn, SearchResultColumn

TEXTS: list[str] = ["Solar energy, solar!", "carbon energy", "Carbon climate solar"]
# Example of the course: the query "solar energy" gives D1 = 0.99, D2 = 0.25 and D3 = 0.
COURSE_TEXTS: list[str] = ["solar energy solar", "carbon energy", "carbon climate"]
COURSE_QUERY: str = "solar energy"
COURSE_SCORES: list[float] = [0.985, 0.245]
SCORE_TOLERANCE: float = 1e-3
NB_DOCUMENTS: int = 10


@pytest.fixture
def search_engine(load_corpus: Callable[[list[str]], Corpus]) -> SearchEngine:
    """Return an engine on a small corpus."""
    return SearchEngine(load_corpus(TEXTS))


def test_index_is_built_at_instantiation(search_engine: SearchEngine) -> None:
    """The matrices are ready as soon as the engine exists."""
    assert search_engine.index.mat_tfidf.shape == (3, 4)


def test_frequencies_has_expected_columns(search_engine: SearchEngine) -> None:
    """The frequencies table has the word, term frequency and document frequency columns."""
    assert list(search_engine.get_frequencies().columns) == list(FrequencyColumn)


def test_frequencies_gives_term_and_document_frequencies(search_engine: SearchEngine) -> None:
    """"solar" occurs 3 times in 2 documents."""
    frequencies: pd.DataFrame = search_engine.get_frequencies().set_index(FrequencyColumn.WORD)
    assert frequencies.loc["solar"].tolist() == [3, 2]


def test_print_statistics_prints_number_of_different_words(
    search_engine: SearchEngine, capsys: pytest.CaptureFixture[str]
) -> None:
    """The statistics start with the size of the vocabulary."""
    search_engine.print_statistics(2)
    assert capsys.readouterr().out.startswith("Number of different words: 4\n")


def test_print_statistics_prints_most_frequent_words_first(
    search_engine: SearchEngine, capsys: pytest.CaptureFixture[str]
) -> None:
    """The most frequent words are printed by decreasing term frequency."""
    search_engine.print_statistics(2)
    lines: list[str] = capsys.readouterr().out.splitlines()
    assert [line.split()[0] for line in lines[3:]] == ["solar", "carbon"]


@pytest.fixture
def course_engine(load_corpus: Callable[[list[str]], Corpus]) -> SearchEngine:
    """Return an engine on the example of the course."""
    return SearchEngine(load_corpus(COURSE_TEXTS))


def test_search_has_expected_columns(course_engine: SearchEngine) -> None:
    """The results table has the `SearchResultColumn` columns."""
    assert list(course_engine.search(COURSE_QUERY, NB_DOCUMENTS).columns) == list(SearchResultColumn)


def test_search_gives_cosine_similarity_of_course(course_engine: SearchEngine) -> None:
    """D1 and D2 get the cosine similarities computed in the course; D3 (null score) is left out."""
    scores: list[float] = course_engine.search(COURSE_QUERY, NB_DOCUMENTS)[SearchResultColumn.SCORE].tolist()
    assert scores == pytest.approx(COURSE_SCORES, abs=SCORE_TOLERANCE)


def test_search_ranks_documents_by_decreasing_score(course_engine: SearchEngine) -> None:
    """The most similar document comes first."""
    assert course_engine.search(COURSE_QUERY, NB_DOCUMENTS)[SearchResultColumn.DOCUMENT_ID].tolist() == [0, 1]


def test_search_returns_at_most_nb_documents(course_engine: SearchEngine) -> None:
    """Only the best documents are returned."""
    assert len(course_engine.search(COURSE_QUERY, 1)) == 1


def test_search_cleans_keywords_like_documents(course_engine: SearchEngine) -> None:
    """Case and punctuation of the query do not change the results."""
    results: pd.DataFrame = course_engine.search("SOLAR, Energy!", NB_DOCUMENTS)
    assert results.equals(course_engine.search(COURSE_QUERY, NB_DOCUMENTS))


def test_search_ignores_unknown_words(course_engine: SearchEngine) -> None:
    """Words missing from the vocabulary do not prevent the search."""
    assert course_engine.search("solar photovoltaic", NB_DOCUMENTS)[SearchResultColumn.DOCUMENT_ID].tolist() == [0]


def test_search_with_only_unknown_words_returns_no_document(course_engine: SearchEngine) -> None:
    """A query sharing no word with the corpus gives an empty table."""
    assert course_engine.search("photovoltaic", NB_DOCUMENTS).empty


def test_search_rejects_query_without_words(course_engine: SearchEngine) -> None:
    """A query made of punctuation only holds no word."""
    with pytest.raises(EmptyQueryError):
        course_engine.search(" ?! ", NB_DOCUMENTS)


def test_search_rejects_non_positive_nb_documents(course_engine: SearchEngine) -> None:
    """At least one document must be asked."""
    with pytest.raises(InvalidNbDocumentsError):
        course_engine.search(COURSE_QUERY, 0)
