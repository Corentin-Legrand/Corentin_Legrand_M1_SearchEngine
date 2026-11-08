"""Document coming from Reddit."""

from dataclasses import dataclass

from models.document import Document
from models.document_origin import DocumentOrigin


@dataclass
class RedditDocument(Document):
    """
    Reddit post.

    Attributes:
        nb_comments (int): Number of comments of the post.

    Author: Corentin Legrand
    """

    nb_comments: int

    @property
    def type(self) -> DocumentOrigin:
        """DocumentOrigin: Always `DocumentOrigin.REDDIT`."""
        return DocumentOrigin.REDDIT
