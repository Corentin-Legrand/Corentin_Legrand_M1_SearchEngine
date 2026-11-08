"""Okapi BM25 score."""

import numpy as np
from scipy.sparse import csr_matrix

from models.term_index import TermIndex
from service.interfaces.i_similarity import ISimilarity

DEFAULT_K1: float = 1.2
DEFAULT_B: float = 0.75
SMOOTHING: float = 0.5


class Bm25Similarity(ISimilarity):
    """
    Score the documents with Okapi BM25.

    For a query Q and a document D, `score = sum over q in Q of IDF(q) * f (k1 + 1) / (f + k1 (1 - b + b |D| / avgdl))`
    where `f` is the number of occurrences of `q` in `D`, `|D|` the length of `D` and `avgdl` the average length.
    `IDF(q) = ln((N - n + 0.5) / (n + 0.5) + 1)`, `n` being the number of documents holding `q`. The weight of
    each word in each document does not depend on the query: it is computed once, in a sparse matrix.

    Attributes:
        mat_bm25 (csr_matrix): BM25 weight of each word in each document (read only).

    Author: Corentin Legrand
    """

    def __init__(self, index: TermIndex, k1: float = DEFAULT_K1, b: float = DEFAULT_B) -> None:
        """Build the measure and the BM25 weights of the corpus.

        Args:
            index (TermIndex): Vocabulary and matrices of the corpus.
            k1 (float): Saturation of the term frequency, usually between 1.2 and 2.
            b (float): Weight of the normalisation by the document length, between 0 (none) and 1 (full).
        """
        self.__mat_bm25: csr_matrix = self.__build_weights(index.mat_tf, k1, b)

    @property
    def mat_bm25(self) -> csr_matrix:
        """csr_matrix: BM25 weight of each word in each document."""
        return self.__mat_bm25

    def compute_scores(self, query_counts: np.ndarray) -> np.ndarray:
        """Compute the BM25 score of each document; each word of the query counts once.

        Args:
            query_counts (np.ndarray): Number of occurrences in the query of each word of the vocabulary.

        Returns:
            np.ndarray: The score of each document, by matrix row, positive and unbounded.
        """
        return self.__mat_bm25 @ (query_counts > 0).astype(float)

    @staticmethod
    def __build_weights(mat_tf: csr_matrix, k1: float, b: float) -> csr_matrix:
        """Compute the BM25 weight of the non null cells of the TF matrix.

        Args:
            mat_tf (csr_matrix): Number of occurrences of each word in each document.
            k1 (float): Saturation of the term frequency.
            b (float): Weight of the normalisation by the document length.

        Returns:
            csr_matrix: The matrix of the same shape whose cell (i, j) is the weight of word j in document i.
        """
        nb_documents: int = mat_tf.shape[0]
        document_frequencies: np.ndarray = mat_tf.getnnz(axis=0)
        idf: np.ndarray = np.log(
            (nb_documents - document_frequencies + SMOOTHING) / (document_frequencies + SMOOTHING) + 1
        )
        lengths: np.ndarray = np.asarray(mat_tf.sum(axis=1)).ravel()
        average_length: float = float(lengths.mean()) if nb_documents else 0.0
        cell_rows: np.ndarray = np.repeat(np.arange(nb_documents), np.diff(mat_tf.indptr))
        frequencies: np.ndarray = mat_tf.data.astype(float)
        length_norms: np.ndarray = k1 * (1 - b + b * lengths[cell_rows] / average_length)
        weights: np.ndarray = idf[mat_tf.indices] * frequencies * (k1 + 1) / (frequencies + length_norms)
        return csr_matrix((weights, mat_tf.indices, mat_tf.indptr), shape=mat_tf.shape)
