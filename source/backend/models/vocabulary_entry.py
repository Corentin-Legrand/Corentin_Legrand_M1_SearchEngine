"""Information about a word of the vocabulary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VocabularyEntry:
    """
    Description of a word of the corpus vocabulary.

    Attributes:
        identifier (int): Unique id of the word, which is also its column in the Documents x Terms matrices.
        nb_occurrences (int): Total number of occurrences of the word in the corpus (term frequency).
        nb_documents (int): Number of documents holding the word (document frequency).

    Author: Corentin Legrand
    """

    identifier: int
    nb_occurrences: int
    nb_documents: int
