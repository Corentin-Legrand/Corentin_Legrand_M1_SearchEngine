"""Application entry point: loads the corpus, displays it and its word statistics, then searches it."""

from helpers.environment_manager import EnvironmentManager
from infrastructure.json_dao import JsonDAO
from infrastructure.json_reader import JsonReader
from infrastructure.json_writer import JsonWriter
from models.corpus import Corpus
from script.scrap_data import DATA_FILENAME_KEY
from script.search_corpus import SearchCorpus
from service.author_manager import AuthorManager
from service.corpus_manager import CorpusManager
from service.corpus_mapper import CorpusMapper
from service.document_factory import DocumentFactory
from service.search_engine import SearchEngine

NB_DOCUMENTS_DISPLAYED: int = 5
NB_WORDS_DISPLAYED: int = 10


def main() -> None:
    """Load the corpus without calling the APIs, print documents and word statistics, then run the search."""
    data_filename: str = EnvironmentManager.get_instance().get_environment_variable(DATA_FILENAME_KEY)
    mapper: CorpusMapper = CorpusMapper(DocumentFactory(), AuthorManager())
    corpus_manager: CorpusManager = CorpusManager(JsonDAO(JsonWriter(), JsonReader()), mapper, data_filename)
    corpus_manager.load()
    print(repr(corpus_manager))

    print(f"\n{NB_DOCUMENTS_DISPLAYED} most recent documents:")
    corpus_manager.print_document_by_date(NB_DOCUMENTS_DISPLAYED, ascending=False)
    print(f"\n{NB_DOCUMENTS_DISPLAYED} first documents by title:")
    corpus_manager.print_document_by_title(NB_DOCUMENTS_DISPLAYED)

    print()
    search_engine: SearchEngine = SearchEngine(Corpus.get_instance())
    search_engine.print_statistics(NB_WORDS_DISPLAYED)
    SearchCorpus(search_engine).run()


if __name__ == "__main__":
    main()
