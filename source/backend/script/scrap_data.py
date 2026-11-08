"""Script fetching documents from Reddit and Arxiv and storing them."""

from helpers.environment_manager import EnvironmentManager
from infrastructure.arxiv_source import ArxivSource
from infrastructure.json_dao import JsonDAO
from infrastructure.json_reader import JsonReader
from infrastructure.json_writer import JsonWriter
from infrastructure.reddit_source import RedditSource
from service.scraping_service import ScrapingService

TOPICS: list[str] = ["climate", "nintendo", "football", "machine learning", "quantum computing"]
MAX_RESULTS_PER_SEARCH: int = 1000
DATA_FILENAME_KEY: str = "DATABASE_FILENAME"


class ScrapData:
    """
    Script gathering the documents about the topics into the storage.

    Attributes:
        scraping_service (ScrapingService): Service doing the gathering (private).

    Author: Corentin Legrand
    """

    def __init__(self, scraping_service: ScrapingService) -> None:
        """Build the script.

        Args:
            scraping_service (ScrapingService): Service doing the gathering.
        """
        self.__scraping_service: ScrapingService = scraping_service

    def run(self, data_filename: str) -> None:
        """Gather the documents about the topics.

        Args:
            data_filename (str): The name of the file storing the documents.
        """
        self.__scraping_service.scrap(TOPICS, MAX_RESULTS_PER_SEARCH, data_filename)


if __name__ == "__main__":
    dao: JsonDAO = JsonDAO(JsonWriter(), JsonReader())
    scraping_service: ScrapingService = ScrapingService([RedditSource(), ArxivSource()], dao)
    data_filename: str = EnvironmentManager.get_instance().get_environment_variable(DATA_FILENAME_KEY)
    ScrapData(scraping_service).run(data_filename)
