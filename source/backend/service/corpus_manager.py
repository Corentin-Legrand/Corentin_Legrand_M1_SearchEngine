"""Management of the unique corpus: loading, saving and displays."""

from collections.abc import Callable
from typing import Any

import pandas as pd

from models.corpus import Corpus
from models.document import Document
from service.corpus_mapper import CorpusMapper
from service.interfaces.i_dao import IDAO

DATE_DISPLAY_FORMAT: str = "%Y-%m-%d"


class CorpusManager:
    """
    Load, save, clear and display the unique corpus.

    Attributes:
        corpus (Corpus): The unique corpus (private).
        dao (IDAO): Storage of the documents table (private).
        mapper (CorpusMapper): Converter between the documents table and the corpus (private).
        data_filename (str): Name of the file storing the documents (private).

    Author: Corentin Legrand
    """

    def __init__(self, dao: IDAO, mapper: CorpusMapper, data_filename: str) -> None:
        """Build the manager on the unique corpus.

        Args:
            dao (IDAO): Storage of the documents table.
            mapper (CorpusMapper): Converter between the documents table and the corpus.
            data_filename (str): Name of the file storing the documents.
        """
        self.__corpus: Corpus = Corpus.get_instance()
        self.__dao: IDAO = dao
        self.__mapper: CorpusMapper = mapper
        self.__data_filename: str = data_filename

    def clear_corpus(self) -> None:
        """Remove all the documents and authors of the corpus and reset its numbering."""
        self.__corpus.documents.clear()
        self.__corpus.authors.clear()
        self.__corpus.nb_document = 0

    def load(self) -> None:
        """Replace the content of the corpus by the stored documents, without calling the APIs.

        Raises:
            FileNotFoundError: If the data file does not exist.
            UnknownDocumentOriginError: If a stored document comes from an unsupported source.
        """
        frame: pd.DataFrame = self.__dao.read_data(self.__data_filename)
        self.clear_corpus()
        self.__mapper.build_corpus_from_dataframe(frame)

    def save(self) -> None:
        """Store the documents of the corpus in the data file."""
        self.__dao.create_data(self.__mapper.build_dataframe_from_corpus(self.__corpus), self.__data_filename)

    def print_document_by_date(self, nb_documents: int, ascending: bool = True) -> None:
        """Print the documents sorted by publication date.

        Args:
            nb_documents (int): The maximum number of documents to print.
            ascending (bool): True to print the oldest first, False for the newest first.
        """
        for document in self.__get_sorted_documents(lambda document: document.date, nb_documents, ascending):
            print(f"{document.date.strftime(DATE_DISPLAY_FORMAT)} {document}")

    def print_document_by_title(self, nb_documents: int, ascending: bool = True) -> None:
        """Print the documents sorted by title, ignoring the case.

        Args:
            nb_documents (int): The maximum number of documents to print.
            ascending (bool): True for the alphabetical order, False for the reverse one.
        """
        sort_key: Callable[[Document], Any] = lambda document: document.title.casefold()
        for document in self.__get_sorted_documents(sort_key, nb_documents, ascending):
            print(document)

    def __get_sorted_documents(
        self, sort_key: Callable[[Document], Any], nb_documents: int, ascending: bool
    ) -> list[Document]:
        """Return the first documents of the corpus according to a sort key.

        Args:
            sort_key (Callable[[Document], Any]): The value the documents are sorted on.
            nb_documents (int): The maximum number of documents to return.
            ascending (bool): True for the ascending order.

        Returns:
            list[Document]: At most `nb_documents` sorted documents.
        """
        documents: list[Document] = sorted(self.__corpus.documents.values(), key=sort_key, reverse=not ascending)
        return documents[:nb_documents]

    def __repr__(self) -> str:
        """Return a summary of the corpus.

        Returns:
            str: The name of the corpus and its numbers of documents and authors.
        """
        return (
            f"Corpus(name='{self.__corpus.name}', nb_documents={len(self.__corpus.documents)}, "
            f"nb_authors={len(self.__corpus.authors)})"
        )
