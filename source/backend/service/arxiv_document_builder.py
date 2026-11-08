"""Builder of Arxiv documents."""

import pandas as pd

from models.arxiv_document import ArxivDocument
from service.document_builder import DocumentBuilder
from service.document_schema import DocumentColumn


class ArxivDocumentBuilder(DocumentBuilder):
    """
    Build Arxiv documents from document rows.
    Author: Corentin Legrand
    """

    def create_arxiv_document(self, row: pd.Series) -> ArxivDocument:
        """Build an Arxiv document from a row.

        Args:
            row (pd.Series): The document row, with `DocumentColumn` columns.

        Returns:
            ArxivDocument: The Arxiv article.
        """
        return ArxivDocument(**self._build_common_fields(row), co_authors=list(row[DocumentColumn.CO_AUTHORS]))
