"""Route of the search page."""

from flask import render_template, request

from models.search_api_client import SearchApiClient, SearchApiError
from models.search_result import SearchResult
from models.similarity_measure import SimilarityMeasure

SEARCH_TEMPLATE: str = "search.html"
DEFAULT_NB_DOCUMENTS: int = 10
MINIMUM_NB_DOCUMENTS: int = 1
MAXIMUM_NB_DOCUMENTS: int = 100
DEFAULT_MEASURE: SimilarityMeasure = SimilarityMeasure.TF_IDF


class SearchController:
    """
    Read the query typed in the search page, ask the search API and render the results.

    Attributes:
        search_api_client (SearchApiClient): Client of the search API (private).

    Author: Corentin Legrand
    """

    def __init__(self, search_api_client: SearchApiClient) -> None:
        """Build the controller.

        Args:
            search_api_client (SearchApiClient): Client of the search API.
        """
        self.__search_api_client: SearchApiClient = search_api_client

    def show_search_page(self) -> str:
        """Render the search page, with the results of the query when one is typed.

        Returns:
            str: The rendered page.
        """
        keywords: str = request.args.get("keywords", "").strip()
        nb_documents: int = request.args.get("nb_documents", DEFAULT_NB_DOCUMENTS, type=int)
        nb_documents = min(max(nb_documents, MINIMUM_NB_DOCUMENTS), MAXIMUM_NB_DOCUMENTS)
        measure: SimilarityMeasure = self.__read_measure()
        results: list[SearchResult] = []
        error_message: str | None = None
        if keywords:
            try:
                results = self.__search_api_client.search(keywords, nb_documents, measure)
            except SearchApiError as error:
                error_message = str(error)
        return render_template(
            SEARCH_TEMPLATE,
            keywords=keywords,
            nb_documents=nb_documents,
            minimum_nb_documents=MINIMUM_NB_DOCUMENTS,
            maximum_nb_documents=MAXIMUM_NB_DOCUMENTS,
            measure=measure,
            measures=list(SimilarityMeasure),
            results=results,
            error_message=error_message,
        )

    @staticmethod
    def __read_measure() -> SimilarityMeasure:
        """Read the similarity measure chosen in the page.

        Returns:
            SimilarityMeasure: The chosen measure, the default one when missing or unknown.
        """
        measure_value: str = request.args.get("measure", DEFAULT_MEASURE)
        return SimilarityMeasure(measure_value) if measure_value in SimilarityMeasure else DEFAULT_MEASURE
