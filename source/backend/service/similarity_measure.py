"""Similarity measures available to rank the documents."""

from enum import StrEnum


class SimilarityMeasure(StrEnum):
    """
    Similarity measures available to rank the documents.

    Attributes:
        TF_IDF: Cosine similarity between TF x IDF vectors.
        BM25: Okapi BM25 score.

    Author: Corentin Legrand
    """

    TF_IDF = "tfidf"
    BM25 = "bm25"
