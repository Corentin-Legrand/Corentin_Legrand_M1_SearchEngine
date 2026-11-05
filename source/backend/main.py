"""Application entry point: loads the stored documents into the corpus and displays it."""

from helpers.environment_manager import EnvironmentManager
from infrastructure.json_dao import JsonDAO
from infrastructure.json_reader import JsonReader
from infrastructure.json_writer import JsonWriter
from script.scrap_data import DATA_FILENAME_KEY
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory

NB_DOCUMENTS_DISPLAYED: int = 5


def main() -> None:
    """Load the corpus from the data file, without calling the APIs, then print a few sorted documents."""
    data_filename: str = EnvironmentManager.get_instance().get_environment_variable(DATA_FILENAME_KEY)
    mapper: CorpusMapper = CorpusMapper(DocumentFactory(), AuthorManager())
    corpus_manager: CorpusManager = CorpusManager(JsonDAO(JsonWriter(), JsonReader()), mapper, data_filename)
    corpus_manager.load()
    print(repr(corpus_manager))

    print(f"\n{NB_DOCUMENTS_DISPLAYED} most recent documents:")
    corpus_manager.print_document_by_date(NB_DOCUMENTS_DISPLAYED, ascending=False)
    print(f"\n{NB_DOCUMENTS_DISPLAYED} first documents by title:")
    corpus_manager.print_document_by_title(NB_DOCUMENTS_DISPLAYED)


if __name__ == "__main__":
    main()
