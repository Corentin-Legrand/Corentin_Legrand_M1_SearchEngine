"""Web interface entry point: serves the search page, which queries the backend search API."""

import os

from flask import Flask

from controllers.search_controller import SearchController
from models.search_api_client import SearchApiClient

API_URL_KEY: str = "SEARCH_API_URL"
DEFAULT_API_URL: str = "http://127.0.0.1:8000"
APP_HOST_KEY: str = "APP_HOST"
DEFAULT_APP_HOST: str = "127.0.0.1"
APP_PORT: int = 5000


def create_app(search_api_client: SearchApiClient) -> Flask:
    """Build the web interface.

    Args:
        search_api_client (SearchApiClient): Client of the search API.

    Returns:
        Flask: The application, serving the search page at its root.
    """
    app: Flask = Flask(__name__)
    search_controller: SearchController = SearchController(search_api_client)
    app.add_url_rule("/", view_func=search_controller.show_search_page)
    return app


if __name__ == "__main__":
    api_url: str = os.environ.get(API_URL_KEY, DEFAULT_API_URL)
    app_host: str = os.environ.get(APP_HOST_KEY, DEFAULT_APP_HOST)
    create_app(SearchApiClient(api_url)).run(host=app_host, port=APP_PORT)
