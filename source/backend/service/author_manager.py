"""Management of the authors of the corpus."""

from models.author import Author
from models.author_stats import AuthorStats
from models.corpus import Corpus
from models.document import Document


class AuthorNotFoundError(KeyError):
    """
    Raised when an author is not part of the corpus.
    Author: Corentin Legrand
    """


class AuthorManager:
    """
    Register the documents of the authors of the corpus and compute their statistics.

    Attributes:
        corpus (Corpus): The unique corpus holding the authors (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the manager on the unique corpus."""
        self.__corpus: Corpus = Corpus.get_instance()

    def add_document_to_author(self, author_name: str, document_id: int, document: Document) -> None:
        """Add a document to the production of an author, registering the author if new.

        The document is linked to the corpus' author, so that each author exists once.

        Args:
            author_name (str): The name of the author.
            document_id (int): The id of the document in the corpus.
            document (Document): The document written by the author.
        """
        if author_name not in self.__corpus.authors:
            self.__corpus.authors[author_name] = Author(author_name)
        author: Author = self.__corpus.authors[author_name]
        author.production[document_id] = document
        author.nb_docs += 1
        document.author = author

    def get_author_stats(self, key: str) -> AuthorStats:
        """Compute the statistics of an author.

        Args:
            key (str): The name of the author.

        Returns:
            AuthorStats: The number of documents and their average number of characters.

        Raises:
            AuthorNotFoundError: If the author is not part of the corpus.
        """
        if key not in self.__corpus.authors:
            raise AuthorNotFoundError(f"Author '{key}' is not part of the corpus.")
        author: Author = self.__corpus.authors[key]
        total_size: int = sum(len(document.text) for document in author.production.values())
        return AuthorStats(nb_document=author.nb_docs, average_size=round(total_size / author.nb_docs))
