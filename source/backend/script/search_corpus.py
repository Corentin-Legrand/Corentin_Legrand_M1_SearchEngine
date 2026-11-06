"""Script asking keywords to the user and printing the matching documents."""

import pandas as pd

from service.search_engine import EmptyQueryError, SearchEngine
from service.text_analysis_schema import SearchResultColumn

NB_RESULTS: int = 10
KEYWORDS_PROMPT: str = "\nKeywords (empty to quit): "
NO_RESULT_MESSAGE: str = "No document matches these keywords."
DISPLAYED_COLUMNS: list[SearchResultColumn] = [
    SearchResultColumn.SCORE,
    SearchResultColumn.ORIGIN,
    SearchResultColumn.TITLE,
]
SCORE_FORMAT: str = "{:.3f}"
TITLE_MAX_WIDTH: int = 90


class SearchCorpus:
    """
    Script searching the corpus with the keywords typed by the user, until an empty line.

    Attributes:
        search_engine (SearchEngine): Engine searching the corpus (private).

    Author: Corentin Legrand
    """

    def __init__(self, search_engine: SearchEngine) -> None:
        """Build the script.

        Args:
            search_engine (SearchEngine): Engine searching the corpus.
        """
        self.__search_engine: SearchEngine = search_engine

    def run(self) -> None:
        """Ask keywords and print the most relevant documents, until the user types an empty line."""
        keywords: str = input(KEYWORDS_PROMPT).strip()
        while keywords:
            self.__print_results(keywords)
            keywords = input(KEYWORDS_PROMPT).strip()

    def __print_results(self, keywords: str) -> None:
        """Print the most relevant documents for keywords.

        Args:
            keywords (str): The words of the query.
        """
        try:
            results: pd.DataFrame = self.__search_engine.search(keywords, NB_RESULTS)
        except EmptyQueryError as error:
            print(error)
        else:
            print(self.__format_results(results))

    @staticmethod
    def __format_results(results: pd.DataFrame) -> str:
        """Format search results for the console.

        Args:
            results (pd.DataFrame): The search results, with `SearchResultColumn` columns.

        Returns:
            str: The score, origin and title of each result, or a message if there is none.
        """
        formatted_results: str = NO_RESULT_MESSAGE
        if not results.empty:
            formatted_results = results[DISPLAYED_COLUMNS].to_string(
                index=False,
                formatters={SearchResultColumn.SCORE: SCORE_FORMAT.format},
                max_colwidth=TITLE_MAX_WIDTH,
            )
        return formatted_results
