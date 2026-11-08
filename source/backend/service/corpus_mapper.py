"""Conversion between the documents table and the corpus."""

from typing import Any

import pandas as pd

from models.arxiv_document import ArxivDocument
from models.corpus import Corpus
from models.document import Document
from models.reddit_document import RedditDocument
from service.author_manager import AuthorManager
from service.document_factory import DocumentFactory
from service.document_schema import DocumentColumn


class CorpusMapper:
    """
    Fill the corpus from a documents table, and turn a corpus back into a documents table.

    Attributes:
        corpus (Corpus): The unique corpus filled by the mapper (private).
        document_factory (DocumentFactory): Factory creating the documents from the rows (private).
        author_manager (AuthorManager): Manager registering the authors of the documents (private).

    Author: Corentin Legrand
    """

    def __init__(self, document_factory: DocumentFactory, author_manager: AuthorManager) -> None:
        """Build the mapper on the unique corpus.

        Args:
            document_factory (DocumentFactory): Factory creating the documents from the rows.
            author_manager (AuthorManager): Manager registering the authors of the documents.
        """
        self.__corpus: Corpus = Corpus.get_instance()
        self.__document_factory: DocumentFactory = document_factory
        self.__author_manager: AuthorManager = author_manager

    def build_corpus_from_dataframe(self, frame: pd.DataFrame) -> Corpus:
        """Add the documents of a table to the corpus, numbering them sequentially.

        Args:
            frame (pd.DataFrame): The documents table, with `DocumentColumn` columns.

        Returns:
            Corpus: The unique corpus, holding the new documents and their authors.

        Raises:
            UnknownDocumentOriginError: If a row comes from an unsupported source.
        """
        for _, row in frame.iterrows():
            document: Document = self.__document_factory.create_document(row)
            document_id: int = self.__corpus.nb_document
            self.__corpus.documents[document_id] = document
            self.__corpus.nb_document += 1
            self.__author_manager.add_document_to_author(document.author.name, document_id, document)
        return self.__corpus

    def build_dataframe_from_corpus(self, corpus: Corpus) -> pd.DataFrame:
        """Turn the documents of a corpus into a documents table.

        Args:
            corpus (Corpus): The corpus to convert.

        Returns:
            pd.DataFrame: One row per document, with `DocumentColumn` columns.
        """
        rows: list[dict[str, Any]] = [self.__build_row(document) for document in corpus.documents.values()]
        return pd.DataFrame(rows, columns=list(DocumentColumn))

    def __build_row(self, document: Document) -> dict[str, Any]:
        """Convert a document into a document row.

        Args:
            document (Document): The document to convert.

        Returns:
            dict[str, Any]: The document row; the columns specific to another source are left empty.
        """
        row: dict[str, Any] = {
            DocumentColumn.TITLE: document.title,
            DocumentColumn.AUTHOR: document.author.name,
            DocumentColumn.DATE: document.date,
            DocumentColumn.URL: document.url,
            DocumentColumn.TEXT: document.text,
            DocumentColumn.ORIGIN: document.type.value,
        }
        match document:
            case RedditDocument():
                row[DocumentColumn.NB_COMMENTS] = document.nb_comments
            case ArxivDocument():
                row[DocumentColumn.CO_AUTHORS] = document.co_authors
        return row
