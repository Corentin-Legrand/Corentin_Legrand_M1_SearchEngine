"""Tests of the search page."""

from datetime import datetime, timezone

import pytest
from flask.testing import FlaskClient

from app import create_app
from controllers.search_controller import MAXIMUM_NB_DOCUMENTS
from models.search_api_client import SearchApiClient, SearchApiError
from models.search_result import SearchResult

FAKE_API_URL: str = "http://fake-api"
FOUND_TITLE: str = "Solar energy in Europe"
UNAVAILABLE_MESSAGE: str = "API down"


class FakeSearchApiClient(SearchApiClient):
    """
    Search API client answering without network, recording the received queries.

    Attributes:
        results (list[SearchResult]): The results returned to every query.
        error (SearchApiError | None): The error raised by every query, if any.
        queries (list[tuple[str, int]]): The received keywords and numbers of documents.

    Author: Corentin Legrand
    """

    def __init__(self, results: list[SearchResult], error: SearchApiError | None = None) -> None:
        """Build the fake client.

        Args:
            results (list[SearchResult]): The results returned to every query.
            error (SearchApiError | None): The error raised by every query, if any.
        """
        super().__init__(FAKE_API_URL)
        self.results: list[SearchResult] = results
        self.error: SearchApiError | None = error
        self.queries: list[tuple[str, int]] = []

    def search(self, keywords: str, nb_documents: int) -> list[SearchResult]:
        """Record the query and return the configured results.

        Args:
            keywords (str): The words of the query.
            nb_documents (int): The maximum number of documents to return.

        Returns:
            list[SearchResult]: The configured results.

        Raises:
            SearchApiError: If an error is configured.
        """
        self.queries.append((keywords, nb_documents))
        if self.error is not None:
            raise self.error
        return self.results


FOUND_RESULT: SearchResult = SearchResult(
    0.9, 0, FOUND_TITLE, "author", datetime(2026, 1, 1, tzinfo=timezone.utc), "arxiv", "https://example.com/0"
)


def build_client(api_client: FakeSearchApiClient) -> FlaskClient:
    """Return a test client of the interface using a fake search API.

    Args:
        api_client (FakeSearchApiClient): The fake search API client.

    Returns:
        FlaskClient: The test client.
    """
    return create_app(api_client).test_client()


def get_page(api_client: FakeSearchApiClient, query_string: dict[str, str | int]) -> str:
    """Return the search page rendered for a query.

    Args:
        api_client (FakeSearchApiClient): The fake search API client.
        query_string (dict[str, str | int]): The parameters of the page.

    Returns:
        str: The rendered page.
    """
    return build_client(api_client).get("/", query_string=query_string).get_data(as_text=True)


def test_page_without_query_does_not_search() -> None:
    """Opening the page does not query the API."""
    api_client: FakeSearchApiClient = FakeSearchApiClient([FOUND_RESULT])
    build_client(api_client).get("/")
    assert api_client.queries == []


def test_page_displays_found_title() -> None:
    """The title of a found document is displayed."""
    assert FOUND_TITLE in get_page(FakeSearchApiClient([FOUND_RESULT]), {"keywords": "solar"})


def test_page_displays_message_without_result() -> None:
    """A query matching nothing displays a message."""
    assert "Aucun document ne correspond" in get_page(FakeSearchApiClient([]), {"keywords": "photovoltaic"})


def test_page_displays_api_error() -> None:
    """An error of the API is displayed instead of results."""
    api_client: FakeSearchApiClient = FakeSearchApiClient([], SearchApiError(UNAVAILABLE_MESSAGE))
    assert UNAVAILABLE_MESSAGE in get_page(api_client, {"keywords": "solar"})


@pytest.mark.parametrize(
    ("nb_documents", "expected"), [(5, 5), (0, 1), (MAXIMUM_NB_DOCUMENTS + 1, MAXIMUM_NB_DOCUMENTS)]
)
def test_page_bounds_number_of_documents(nb_documents: int, expected: int) -> None:
    """The number of documents sent to the API stays within the bounds."""
    api_client: FakeSearchApiClient = FakeSearchApiClient([])
    get_page(api_client, {"keywords": "solar", "nb_documents": nb_documents})
    assert api_client.queries == [("solar", expected)]
