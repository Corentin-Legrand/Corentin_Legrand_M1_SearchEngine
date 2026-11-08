"""Web API entry point: loads the corpus, builds the search engine once, then serves it over HTTP."""

import uvicorn
from fastapi import FastAPI

from controller.search_controller import SearchController
from helpers.environment_manager import EnvironmentManager
from infrastructure.json_dao import JsonDAO
from infrastructure.json_reader import JsonReader
from infrastructure.json_writer import JsonWriter
from models.corpus import Corpus
from script.scrap_data import DATA_FILENAME_KEY
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory
from service.search_engine import EmptyQueryError, InvalidNbDocumentsError, SearchEngine

API_TITLE: str = "Search engine API"
API_HOST: str = "127.0.0.1"
API_PORT: int = 8000


def create_app(search_engine: SearchEngine) -> FastAPI:
    """Build the web application exposing a search engine.

    Args:
        search_engine (SearchEngine): The engine answering the queries.

    Returns:
        FastAPI: The application, with its routes and error handlers.
    """
    app: FastAPI = FastAPI(title=API_TITLE)
    search_controller: SearchController = SearchController(search_engine)
    app.include_router(search_controller.router)
    app.add_exception_handler(EmptyQueryError, SearchController.handle_invalid_query)
    app.add_exception_handler(InvalidNbDocumentsError, SearchController.handle_invalid_query)
    return app


def build_app() -> FastAPI:
    """Load the saved corpus without calling the APIs and build the application searching it.

    The matrices are built here, once, before the server accepts requests.

    Returns:
        FastAPI: The application searching the saved corpus.
    """
    data_filename: str = EnvironmentManager.get_instance().get_environment_variable(DATA_FILENAME_KEY)
    mapper: CorpusMapper = CorpusMapper(DocumentFactory(), AuthorManager())
    CorpusManager(JsonDAO(JsonWriter(), JsonReader()), mapper, data_filename).load()
    return create_app(SearchEngine(Corpus.get_instance()))


if __name__ == "__main__":
    uvicorn.run(build_app(), host=API_HOST, port=API_PORT)
