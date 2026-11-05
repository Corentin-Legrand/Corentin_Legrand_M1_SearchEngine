"""Application entry point: imports the documents then reloads them."""

import pandas as pd

from helpers.environment_manager import EnvironmentManager
from infrastructure.arxiv_source import ArxivSource
from infrastructure.json_dao import JsonDAO
from infrastructure.json_reader import JsonReader
from infrastructure.json_writer import JsonWriter
from infrastructure.reddit_source import RedditSource
from script.scrap_data import DATA_FILENAME_KEY, ScrapData
from service.interfaces.i_dao import IDAO
from service.scraping_service import ScrapingService


def main() -> None:
    """Run the import script, reload the stored documents and print their number."""
    dao: IDAO = JsonDAO(JsonWriter(), JsonReader())
    data_filename: str = EnvironmentManager.get_instance().get_environment_variable(DATA_FILENAME_KEY)

    scraping_service: ScrapingService = ScrapingService([RedditSource(), ArxivSource()], dao)
    ScrapData(scraping_service).run(data_filename)

    documents: pd.DataFrame = dao.read_data(data_filename)
    print(f"Number of documents: {len(documents)}")


if __name__ == "__main__":
    main()
