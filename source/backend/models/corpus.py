"""Structure of the unique corpus."""

from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import ClassVar

from helpers.environment_manager import SingletonInstantiationError
from models.author import Author
from models.document import Document

DEFAULT_CORPUS_NAME: str = "corpus"


@dataclass
class Corpus:
    """
    Singleton holding the documents and the authors of the corpus.

    Attributes:
        instance (Corpus | None): The unique instance (private, class scope).
        name (str): Name of the corpus.
        nb_document (int): Counter of the documents added, used to number them.
        documents (dict[int, Document]): Documents of the corpus, by document id.
        authors (dict[str, Author]): Authors of the corpus, by name.

    Author: Corentin Legrand
    """

    __instance: ClassVar[Corpus | None] = None
    __CREATION_KEY: ClassVar[object] = object()

    creation_key: InitVar[object]
    name: str = DEFAULT_CORPUS_NAME
    nb_document: int = 0
    documents: dict[int, Document] = field(default_factory=dict)
    authors: dict[str, Author] = field(default_factory=dict)

    def __post_init__(self, creation_key: object) -> None:
        """Check that the corpus is built by `get_instance`.

        Args:
            creation_key (object): Private key only known by `get_instance`.

        Raises:
            SingletonInstantiationError: If called outside `get_instance`.
        """
        if creation_key is not Corpus.__CREATION_KEY:
            raise SingletonInstantiationError("Corpus is a singleton, use Corpus.get_instance().")

    @classmethod
    def get_instance(cls) -> Corpus:
        """Return the unique corpus, creating it on first call.

        Returns:
            Corpus: The unique corpus.
        """
        if cls.__instance is None:
            cls.__instance = cls(cls.__CREATION_KEY)
        return cls.__instance
