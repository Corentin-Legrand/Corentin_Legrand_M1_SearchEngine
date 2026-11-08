"""Similarity measures offered by the search API."""

from enum import StrEnum


class SimilarityMeasure(StrEnum):
    """
    Similarity measures offered by the search API; the value is the one expected by the API.

    Attributes:
        TF_IDF: Cosine similarity between TF x IDF vectors.
        BM25: Okapi BM25 score.

    Author: Corentin Legrand
    """

    TF_IDF = "tfidf"
    BM25 = "bm25"

    @property
    def label(self) -> str:
        """str: Name of the measure displayed to the user."""
        return MEASURE_LABELS[self]


MEASURE_LABELS: dict[SimilarityMeasure, str] = {
    SimilarityMeasure.TF_IDF: "TF-IDF (cosinus)",
    SimilarityMeasure.BM25: "Okapi BM25",
}
