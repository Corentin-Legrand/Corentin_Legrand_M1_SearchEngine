"""Builder of Reddit documents."""

import pandas as pd

from models.reddit_document import RedditDocument
from service.document_builder import DocumentBuilder
from service.document_schema import DocumentColumn


class RedditDocumentBuilder(DocumentBuilder):
    """
    Build Reddit documents from document rows.
    Author: Corentin Legrand
    """

    def create_reddit_document(self, row: pd.Series) -> RedditDocument:
        """Build a Reddit document from a row.

        Args:
            row (pd.Series): The document row, with `DocumentColumn` columns.

        Returns:
            RedditDocument: The Reddit post.
        """
        return RedditDocument(**self._build_common_fields(row), nb_comments=int(row[DocumentColumn.NB_COMMENTS]))
