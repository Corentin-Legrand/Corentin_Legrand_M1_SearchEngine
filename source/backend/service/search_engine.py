"""Search engine built on the Documents x Terms description of a corpus."""

from collections import Counter
from typing import Any

import numpy as np
import pandas as pd

from helpers.text_manager import TextManager
from models.corpus import Corpus
from models.document import Document
from models.term_index import TermIndex
from service.bm25_similarity import Bm25Similarity
from service.interfaces.i_similarity import ISimilarity
from service.similarity_measure import SimilarityMeasure
from service.term_index_builder import TermIndexBuilder
from service.text_analysis_schema import FrequencyColumn, SearchResultColumn
from service.tfidf_cosine_similarity import TfIdfCosineSimilarity

MINIMUM_NB_DOCUMENTS: int = 1


class EmptyQueryError(ValueError):
    """
    Raised when a query holds no word once cleaned.
    Author: Corentin Legrand
    """


class InvalidNbDocumentsError(ValueError):
    """
    Raised when the number of documents to return is not strictly positive.
    Author: Corentin Legrand
    """


class SearchEngine:
    """
    Search engine over a corpus, whose vocabulary and matrices are built at instantiation.

    Documents are ranked by a `SimilarityMeasure`: the cosine similarity between their TF x IDF vector and the one
    of the query (default), or the Okapi BM25 score.

    Attributes:
        index (TermIndex): Vocabulary and Documents x Terms matrices of the corpus (read only).
        corpus (Corpus): The searched corpus (private).
        similarities (dict[SimilarityMeasure, ISimilarity]): The available similarity measures (private).
        text_manager (TextManager): Helper cleaning and splitting the queries (private).

    Author: Corentin Legrand
    """

    def __init__(self, corpus: Corpus) -> None:
        """Build the engine and the Documents x Terms matrices of a corpus.

        Args:
            corpus (Corpus): The corpus to search.
        """
        self.__corpus: Corpus = corpus
        self.__index: TermIndex = TermIndexBuilder().build(corpus)
        self.__similarities: dict[SimilarityMeasure, ISimilarity] = {
            SimilarityMeasure.TF_IDF: TfIdfCosineSimilarity(self.__index),
            SimilarityMeasure.BM25: Bm25Similarity(self.__index),
        }
        self.__text_manager: TextManager = TextManager()

    @property
    def index(self) -> TermIndex:
        """TermIndex: Vocabulary and Documents x Terms matrices of the corpus."""
        return self.__index

    def search(
        self, keywords: str, nb_documents: int, measure: SimilarityMeasure = SimilarityMeasure.TF_IDF
    ) -> pd.DataFrame:
        """Return the documents most similar to a query.

        The keywords are cleaned like the documents; the words missing from the vocabulary are ignored.

        Args:
            keywords (str): The words of the query.
            nb_documents (int): The maximum number of documents to return.
            measure (SimilarityMeasure): The measure ranking the documents.

        Returns:
            pd.DataFrame: The documents of non null score, by decreasing score, with `SearchResultColumn` columns.

        Raises:
            EmptyQueryError: If the query holds no word once cleaned.
            InvalidNbDocumentsError: If `nb_documents` is not strictly positive.
        """
        if nb_documents < MINIMUM_NB_DOCUMENTS:
            raise InvalidNbDocumentsError(f"The number of documents must be positive, got {nb_documents}.")
        scores: np.ndarray = self.__similarities[measure].compute_scores(self.__count_query_words(keywords))
        ranked_rows: np.ndarray = np.argsort(-scores, kind="stable")
        best_rows: list[int] = [int(row) for row in ranked_rows[:nb_documents] if scores[row] > 0]
        rows: list[dict[str, Any]] = [self.__build_result(row, float(scores[row])) for row in best_rows]
        return pd.DataFrame(rows, columns=list(SearchResultColumn))

    def get_frequencies(self) -> pd.DataFrame:
        """Return the frequencies of the words of the vocabulary.

        Returns:
            pd.DataFrame: One row per word, in alphabetical order, with `FrequencyColumn` columns.
        """
        rows: list[dict[str, str | int]] = [
            {
                FrequencyColumn.WORD: word,
                FrequencyColumn.TERM_FREQUENCY: entry.nb_occurrences,
                FrequencyColumn.DOCUMENT_FREQUENCY: entry.nb_documents,
            }
            for word, entry in self.__index.vocab.items()
        ]
        return pd.DataFrame(rows, columns=list(FrequencyColumn))

    def print_statistics(self, nb_words: int) -> None:
        """Print the number of different words of the corpus and its most frequent words.

        Args:
            nb_words (int): The number of most frequent words to print.
        """
        frequencies: pd.DataFrame = self.get_frequencies()
        most_frequent_words: pd.DataFrame = frequencies.nlargest(nb_words, FrequencyColumn.TERM_FREQUENCY)
        print(f"Number of different words: {len(frequencies)}")
        print(f"{nb_words} most frequent words:")
        print(most_frequent_words.to_string(index=False))

    def __count_query_words(self, keywords: str) -> np.ndarray:
        """Count the occurrences of the words of the vocabulary in a query.

        Args:
            keywords (str): The words of the query.

        Returns:
            np.ndarray: The number of occurrences in the query of each word of the vocabulary.

        Raises:
            EmptyQueryError: If the query holds no word once cleaned.
        """
        words: list[str] = self.__text_manager.tokenize(self.__text_manager.clean_text(keywords))
        if not words:
            raise EmptyQueryError(f"The query '{keywords}' holds no word.")
        query_counts: np.ndarray = np.zeros(len(self.__index.vocab))
        for word, count in Counter(words).items():
            if word in self.__index.vocab:
                query_counts[self.__index.vocab[word].identifier] = count
        return query_counts

    def __build_result(self, row: int, score: float) -> dict[str, Any]:
        """Describe a found document.

        Args:
            row (int): The matrix row of the document.
            score (float): The similarity of the document with the query.

        Returns:
            dict[str, Any]: The result row, with `SearchResultColumn` columns.
        """
        document_id: int = self.__index.document_ids[row]
        document: Document = self.__corpus.documents[document_id]
        return {
            SearchResultColumn.SCORE: score,
            SearchResultColumn.DOCUMENT_ID: document_id,
            SearchResultColumn.TITLE: document.title,
            SearchResultColumn.AUTHOR: document.author.name,
            SearchResultColumn.DATE: document.date,
            SearchResultColumn.ORIGIN: document.type.value,
            SearchResultColumn.URL: document.url,
        }
