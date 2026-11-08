"""Service gathering documents from external sources into the storage."""

import pandas as pd

from helpers.text_manager import TextManager
from service.document_schema import DocumentColumn
from service.interfaces.i_dao import IDAO
from service.interfaces.i_document_source import IDocumentSource


class ScrapingService:
    """
    Fetch documents from several sources, remove the too short ones and store the others.

    Attributes:
        sources (list[IDocumentSource]): Sources the documents are fetched from (private).
        dao (IDAO): Storage of the documents (private).
        text_manager (TextManager): Helper measuring the texts (private).

    Author: Corentin Legrand
    """

    def __init__(self, sources: list[IDocumentSource], dao: IDAO) -> None:
        """Build the service.

        Args:
            sources (list[IDocumentSource]): Sources the documents are fetched from.
            dao (IDAO): Storage of the documents.
        """
        self.__sources: list[IDocumentSource] = sources
        self.__dao: IDAO = dao
        self.__text_manager: TextManager = TextManager()

    def scrap(self, topics: list[str], max_results_per_search: int, data_filename: str) -> None:
        """Fetch the documents matching the topics, filter them and store them.

        Each topic is searched in each source; a document found by several topics is kept once.

        Args:
            topics (list[str]): The topics to search.
            max_results_per_search (int): The maximum number of documents fetched per topic and source.
            data_filename (str): The name of the file storing the documents.
        """
        fetched_documents: list[pd.DataFrame] = [
            source.fetch_documents(topic, max_results_per_search) for topic in topics for source in self.__sources
        ]
        documents: pd.DataFrame = pd.concat(fetched_documents, ignore_index=True)
        documents = documents.drop_duplicates(subset=[DocumentColumn.URL])
        documents = self.__remove_too_short_documents(documents)
        self.__dao.create_data(documents, data_filename)

    def __remove_too_short_documents(self, documents: pd.DataFrame) -> pd.DataFrame:
        """Remove the documents whose text has less than 100 characters.

        Args:
            documents (pd.DataFrame): The documents to filter.

        Returns:
            pd.DataFrame: The documents long enough.
        """
        is_too_short: pd.Series = documents[DocumentColumn.TEXT].map(self.__text_manager.is_too_short)
        return documents[~is_too_short]
