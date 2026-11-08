"""Contract for scoring the documents of a corpus against a query."""

from abc import ABC, abstractmethod

import numpy as np


class ISimilarity(ABC):
    """
    Interface for the similarity measures ranking the documents of a `TermIndex` against a query.
    Author: Corentin Legrand
    """

    @abstractmethod
    def compute_scores(self, query_counts: np.ndarray) -> np.ndarray:
        """Score each document against a query.

        Args:
            query_counts (np.ndarray): Number of occurrences in the query of each word of the vocabulary.

        Returns:
            np.ndarray: The score of each document, by matrix row; the higher, the more relevant, 0 when unrelated.
        """
