"""HTTP routes of the search engine."""

from typing import Annotated, Any

import pandas as pd
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from controller.schemas import ErrorDTO, SearchResultDTO
from service.search_engine import MINIMUM_NB_DOCUMENTS, SearchEngine

SEARCH_PATH: str = "/search"
DEFAULT_NB_DOCUMENTS: int = 10
MAXIMUM_NB_DOCUMENTS: int = 100


class SearchController:
    """
    Expose the search engine over HTTP.

    Attributes:
        router (APIRouter): The routes of the controller, to include in the application (read only).
        search_engine (SearchEngine): The engine answering the queries (private).

    Author: Corentin Legrand
    """

    def __init__(self, search_engine: SearchEngine) -> None:
        """Build the controller and its routes.

        Args:
            search_engine (SearchEngine): The engine answering the queries.
        """
        self.__search_engine: SearchEngine = search_engine
        self.__router: APIRouter = APIRouter()
        self.__router.add_api_route(
            SEARCH_PATH,
            self.search,
            methods=["GET"],
            response_model=list[SearchResultDTO],
            responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorDTO}},
        )

    @property
    def router(self) -> APIRouter:
        """APIRouter: The routes of the controller, to include in the application."""
        return self.__router

    def search(
        self,
        keywords: Annotated[str, Query(description="The words of the query.")],
        nb_documents: Annotated[
            int,
            Query(
                ge=MINIMUM_NB_DOCUMENTS,
                le=MAXIMUM_NB_DOCUMENTS,
                description="The maximum number of documents to return.",
            ),
        ] = DEFAULT_NB_DOCUMENTS,
    ) -> list[SearchResultDTO]:
        """Return the documents most similar to a query, by decreasing score.

        Args:
            keywords (str): The words of the query.
            nb_documents (int): The maximum number of documents to return.

        Returns:
            list[SearchResultDTO]: The found documents, empty when no document matches.
        """
        results: pd.DataFrame = self.__search_engine.search(keywords, nb_documents)
        rows: list[dict[str, Any]] = results.to_dict(orient="records")
        return [SearchResultDTO.model_validate(row) for row in rows]

    @staticmethod
    def handle_invalid_query(request: Request, error: Exception) -> JSONResponse:
        """Turn a query rejected by the search engine into a `400 Bad Request` response.

        Args:
            request (Request): The rejected request.
            error (Exception): The error raised by the search engine.

        Returns:
            JSONResponse: The response describing the error.
        """
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ErrorDTO(detail=str(error)).model_dump())
