"""Construction of the vocabulary and of the Documents x Terms matrices of a corpus."""

from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix

from helpers.text_manager import TextManager
from models.corpus import Corpus
from models.term_index import TermIndex
from models.vocabulary_entry import VocabularyEntry


class TermIndexBuilder:
    """
    Build the vocabulary, the TF matrix and the TF x IDF matrix of a corpus, by hand.

    The texts are cleaned and split only once; the word statistics are then read from the TF matrix.

    Attributes:
        text_manager (TextManager): Helper cleaning and splitting the texts (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the index builder."""
        self.__text_manager: TextManager = TextManager()

    def build(self, corpus: Corpus) -> TermIndex:
        """Describe the documents of a corpus by their words.

        Args:
            corpus (Corpus): The corpus to describe.

        Returns:
            TermIndex: The vocabulary, sorted alphabetically, and the TF and TF x IDF matrices.
        """
        document_ids: list[int] = list(corpus.documents.keys())
        word_counts: list[Counter[str]] = [self.__count_words(corpus.documents[key].text) for key in document_ids]
        words: list[str] = sorted(set().union(*word_counts))
        column_by_word: dict[str, int] = {word: column for column, word in enumerate(words)}

        mat_tf: csr_matrix = self.__build_tf_matrix(word_counts, column_by_word)
        nb_occurrences: np.ndarray = np.asarray(mat_tf.sum(axis=0)).ravel()
        nb_documents: np.ndarray = mat_tf.getnnz(axis=0)
        vocab: dict[str, VocabularyEntry] = {
            word: VocabularyEntry(column, int(nb_occurrences[column]), int(nb_documents[column]))
            for word, column in column_by_word.items()
        }
        idf: np.ndarray = np.log(len(document_ids) / nb_documents)
        mat_tfidf: csr_matrix = csr_matrix(mat_tf.multiply(idf))
        return TermIndex(vocab, document_ids, idf, mat_tf, mat_tfidf)

    def __count_words(self, text: str) -> Counter[str]:
        """Count the occurrences of each word of a text.

        Args:
            text (str): The raw text.

        Returns:
            Counter[str]: The number of occurrences of each word of the cleaned text.
        """
        return Counter(self.__text_manager.tokenize(self.__text_manager.clean_text(text)))

    @staticmethod
    def __build_tf_matrix(word_counts: list[Counter[str]], column_by_word: dict[str, int]) -> csr_matrix:
        """Build the sparse Documents x Terms matrix of the occurrences.

        Args:
            word_counts (list[Counter[str]]): The word occurrences of each document, one per row.
            column_by_word (dict[str, int]): The column of each word.

        Returns:
            csr_matrix: The matrix whose cell (i, j) is the number of occurrences of word j in document i.
        """
        rows: list[int] = []
        columns: list[int] = []
        counts: list[int] = []
        for row, document_word_counts in enumerate(word_counts):
            for word, count in document_word_counts.items():
                rows.append(row)
                columns.append(column_by_word[word])
                counts.append(count)
        shape: tuple[int, int] = (len(word_counts), len(column_by_word))
        return csr_matrix((np.array(counts, dtype=np.int64), (rows, columns)), shape=shape)
