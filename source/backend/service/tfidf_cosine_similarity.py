"""Cosine similarity between TF x IDF vectors."""

import numpy as np

from models.term_index import TermIndex
from service.interfaces.i_similarity import ISimilarity


class TfIdfCosineSimilarity(ISimilarity):
    """
    Score the documents by the cosine of the angle between their TF x IDF vector and the one of the query.

    Attributes:
        index (TermIndex): Vocabulary and matrices of the corpus (private).
        document_norms (np.ndarray): Euclidean norm of the TF x IDF vector of each document (private).

    Author: Corentin Legrand
    """

    def __init__(self, index: TermIndex) -> None:
        """Build the measure and the norm of each document.

        Args:
            index (TermIndex): Vocabulary and matrices of the corpus.
        """
        self.__index: TermIndex = index
        self.__document_norms: np.ndarray = np.sqrt(np.asarray(index.mat_tfidf.power(2).sum(axis=1)).ravel())

    def compute_scores(self, query_counts: np.ndarray) -> np.ndarray:
        """Compute the cosine similarity between a query and each document.

        A document or a query of null norm (no weighted word) has a null similarity.

        Args:
            query_counts (np.ndarray): Number of occurrences in the query of each word of the vocabulary.

        Returns:
            np.ndarray: The similarity of each document, by matrix row, between 0 and 1.
        """
        query_vector: np.ndarray = query_counts * self.__index.idf
        dot_products: np.ndarray = self.__index.mat_tfidf @ query_vector
        norms: np.ndarray = self.__document_norms * np.linalg.norm(query_vector)
        return np.divide(dot_products, norms, out=np.zeros_like(dot_products), where=norms > 0)
