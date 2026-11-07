"""Client of the search API exposed by the backend."""

from datetime import datetime
from typing import Any

import httpx2

from models.search_result import SearchResult

SEARCH_PATH: str = "/search"
REQUEST_TIMEOUT_SECONDS: float = 10.0
UNAVAILABLE_MESSAGE: str = "Le moteur de recherche est injoignable."
REJECTED_MESSAGE: str = "La recherche a été refusée."
JSON_CONTENT_TYPE: str = "application/json"


class SearchApiError(Exception):
    """
    Raised when the search API cannot answer a query.
    Author: Corentin Legrand
    """


class SearchApiClient:
    """
    Query the search API of the backend over HTTP.

    Attributes:
        base_url (str): Address of the backend (private).

    Author: Corentin Legrand
    """

    def __init__(self, base_url: str) -> None:
        """Build the client.

        Args:
            base_url (str): Address of the backend, e.g. `http://127.0.0.1:8000`.
        """
        self.__base_url: str = base_url

    def search(self, keywords: str, nb_documents: int) -> list[SearchResult]:
        """Return the documents most similar to a query, by decreasing score.

        Args:
            keywords (str): The words of the query.
            nb_documents (int): The maximum number of documents to return.

        Returns:
            list[SearchResult]: The found documents, empty when no document matches.

        Raises:
            SearchApiError: If the backend is unreachable or rejects the query.
        """
        parameters: dict[str, str | int] = {"keywords": keywords, "nb_documents": nb_documents}
        try:
            response: httpx2.Response = httpx2.get(
                self.__base_url + SEARCH_PATH, params=parameters, timeout=REQUEST_TIMEOUT_SECONDS
            )
        except httpx2.HTTPError as error:
            raise SearchApiError(UNAVAILABLE_MESSAGE) from error
        if response.is_error:
            raise SearchApiError(self.__get_error_message(response))
        return [self.__build_result(row) for row in response.json()]

    @staticmethod
    def __get_error_message(response: httpx2.Response) -> str:
        """Return the reason of a rejected query.

        Args:
            response (httpx2.Response): The error response of the backend.

        Returns:
            str: The detail given by the backend when it is a sentence, a generic message otherwise.
        """
        is_json: bool = response.headers.get("content-type", "").startswith(JSON_CONTENT_TYPE)
        detail: Any = response.json().get("detail") if is_json else None
        return detail if isinstance(detail, str) else REJECTED_MESSAGE

    @staticmethod
    def __build_result(row: dict[str, Any]) -> SearchResult:
        """Build a search result from its JSON description.

        Args:
            row (dict[str, Any]): A result returned by the backend.

        Returns:
            SearchResult: The result, with a parsed date.
        """
        return SearchResult(**{**row, "date": datetime.fromisoformat(row["date"])})
