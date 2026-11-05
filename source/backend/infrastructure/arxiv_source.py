"""Fetching of documents from Arxiv."""

import ssl
import time
from datetime import datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import xmltodict

from helpers.text_manager import TextManager
from models.document_origin import DocumentOrigin
from service.document_schema import DocumentColumn
from service.interfaces.i_document_source import IDocumentSource

ARXIV_API_URL: str = "https://export.arxiv.org/api/query"
ARXIV_SEARCH_FIELD: str = "all"
ARXIV_TIMEOUT_SECONDS: int = 60
ARXIV_REQUEST_DELAY_SECONDS: int = 3
ARXIV_LIST_TAGS: tuple[str, ...] = ("entry", "author")
HTTP_PROTOCOL: str = "http/1.1"


class ArxivSource(IDocumentSource):
    """
    Fetch Arxiv articles through its Atom API; the text of an article is its `summary`.

    Attributes:
        text_manager (TextManager): Helper cleaning the texts (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the Arxiv source."""
        self.__text_manager: TextManager = TextManager()

    def fetch_documents(self, query: str, max_results: int) -> pd.DataFrame:
        """Search the Arxiv articles matching a query.

        Args:
            query (str): The keywords to search.
            max_results (int): The maximum number of articles to fetch.

        Returns:
            pd.DataFrame: One row per article.
        """
        # Quotes make Arxiv search the whole query as a phrase instead of independent words.
        search_query: str = f'{ARXIV_SEARCH_FIELD}:"{query}"'
        parameters: str = urlencode({"search_query": search_query, "max_results": max_results})
        # Arxiv rejects (HTTP 406) the default TLS handshake of urllib; announcing HTTP/1.1 is accepted.
        tls_context: ssl.SSLContext = ssl.create_default_context()
        tls_context.set_alpn_protocols([HTTP_PROTOCOL])
        # Arxiv asks clients to wait 3 seconds between requests, otherwise it answers HTTP 429.
        time.sleep(ARXIV_REQUEST_DELAY_SECONDS)
        with urlopen(f"{ARXIV_API_URL}?{parameters}", timeout=ARXIV_TIMEOUT_SECONDS, context=tls_context) as response:
            feed: dict[str, Any] = xmltodict.parse(response.read(), force_list=ARXIV_LIST_TAGS)["feed"]
        return pd.DataFrame([self.__build_row(entry) for entry in feed.get("entry", [])])

    def __build_row(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Convert an Arxiv feed entry into a document row.

        Args:
            entry (dict[str, Any]): The parsed Arxiv entry.

        Returns:
            dict[str, Any]: The document row, the first author being the main one.
        """
        author_names: list[str] = [author["name"] for author in entry["author"]]
        return {
            DocumentColumn.TITLE: self.__text_manager.to_single_line(entry["title"]),
            DocumentColumn.AUTHOR: author_names[0],
            DocumentColumn.DATE: datetime.fromisoformat(entry["published"]),
            DocumentColumn.URL: entry["id"],
            DocumentColumn.TEXT: self.__text_manager.to_single_line(entry["summary"]),
            DocumentColumn.ORIGIN: DocumentOrigin.ARXIV.value,
            DocumentColumn.CO_AUTHORS: author_names[1:],
        }
