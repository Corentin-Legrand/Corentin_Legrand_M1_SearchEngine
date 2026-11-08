"""Documents x Terms description of a corpus."""

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix

from models.vocabulary_entry import VocabularyEntry


@dataclass(frozen=True)
class TermIndex:
    """
    Vocabulary and Documents x Terms matrices of a corpus.

    Row `i` of the matrices describes the document `document_ids[i]`; column `j` describes the
    word whose `VocabularyEntry.identifier` is `j`.

    Attributes:
        vocab (dict[str, VocabularyEntry]): Words of the corpus, in alphabetical order.
        document_ids (list[int]): Corpus id of the document of each matrix row.
        idf (np.ndarray): Inverse document frequency of each word, `log(N / df)`.
        mat_tf (csr_matrix): Number of occurrences of each word in each document (TF).
        mat_tfidf (csr_matrix): TF x IDF score of each word in each document.

    Author: Corentin Legrand
    """

    vocab: dict[str, VocabularyEntry]
    document_ids: list[int]
    idf: np.ndarray
    mat_tf: csr_matrix
    mat_tfidf: csr_matrix
