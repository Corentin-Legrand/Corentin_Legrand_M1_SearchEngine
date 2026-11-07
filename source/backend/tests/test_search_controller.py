"""Tests of the HTTP routes of the search engine."""

from collections.abc import Callable

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx2 import Response

from api import create_app
from controller.search_controller import MAXIMUM_NB_DOCUMENTS, SEARCH_PATH
from models.corpus import Corpus
from service.search_engine import SearchEngine

COURSE_TEXTS: list[str] = ["Solar energy, solar!", "carbon energy", "Carbon climate"]
COURSE_QUERY: str = "solar energy"


@pytest.fixture
def client(load_corpus: Callable[[list[str]], Corpus]) -> TestClient:
    """Return a client of the application searching the course corpus."""
    return TestClient(create_app(SearchEngine(load_corpus(COURSE_TEXTS))))


def get_search(client: TestClient, keywords: str, nb_documents: int | None = None) -> Response:
    """Send a search request.

    Args:
        client (TestClient): The client of the application.
        keywords (str): The words of the query.
        nb_documents (int | None): The maximum number of documents to return, the default one when None.

    Returns:
        Response: The response of the application.
    """
    parameters: dict[str, str | int] = {"keywords": keywords}
    if nb_documents is not None:
        parameters["nb_documents"] = nb_documents
    return client.get(SEARCH_PATH, params=parameters)


def test_search_returns_ids_by_decreasing_score(client: TestClient) -> None:
    """The matching documents are returned by decreasing score."""
    results: list[dict[str, object]] = get_search(client, COURSE_QUERY).json()
    assert [result["document_id"] for result in results] == [0, 1]


def test_search_returns_course_scores(client: TestClient) -> None:
    """The scores are the cosine similarities of the course example."""
    results: list[dict[str, object]] = get_search(client, COURSE_QUERY).json()
    assert [result["score"] for result in results] == pytest.approx([0.985, 0.245], abs=1e-3)


def test_search_describes_document(client: TestClient) -> None:
    """Each result describes its document."""
    result: dict[str, object] = get_search(client, COURSE_QUERY).json()[0]
    assert (result["title"], result["origin"], result["url"]) == ("title 0", "reddit", "https://example.com/0")


def test_search_limits_number_of_documents(client: TestClient) -> None:
    """No more documents than requested are returned."""
    assert len(get_search(client, COURSE_QUERY, 1).json()) == 1


def test_search_without_match_returns_empty_list(client: TestClient) -> None:
    """A query matching no document returns an empty list."""
    assert get_search(client, "photovoltaic").json() == []


def test_search_without_words_is_bad_request(client: TestClient) -> None:
    """A query holding no word once cleaned is rejected."""
    assert get_search(client, "?!").status_code == status.HTTP_400_BAD_REQUEST


def test_search_with_too_many_documents_is_rejected(client: TestClient) -> None:
    """A number of documents above the maximum is rejected by the validation."""
    response: Response = get_search(client, COURSE_QUERY, MAXIMUM_NB_DOCUMENTS + 1)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_search_without_keywords_is_rejected(client: TestClient) -> None:
    """The keywords are required."""
    assert client.get(SEARCH_PATH).status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
