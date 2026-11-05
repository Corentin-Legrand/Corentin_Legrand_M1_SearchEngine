"""Data access object persisting DataFrames as JSON files."""

import pandas as pd

from service.interfaces.i_dao import IDAO
from service.interfaces.i_json_reader import IJsonReader
from service.interfaces.i_json_writer import IJsonWriter


class JsonDAO(IDAO):
    """
    Persist DataFrames as JSON files through an injected writer and reader.

    Attributes:
        writer (IJsonWriter): Component writing the JSON files (private).
        reader (IJsonReader): Component reading the JSON files (private).

    Author: Corentin Legrand
    """

    def __init__(self, writer: IJsonWriter, reader: IJsonReader) -> None:
        """Build the DAO from its writer and reader.

        Args:
            writer (IJsonWriter): Component writing the JSON files.
            reader (IJsonReader): Component reading the JSON files.
        """
        self.__writer: IJsonWriter = writer
        self.__reader: IJsonReader = reader

    def create_data(self, content: pd.DataFrame, filename: str) -> None:
        """Store a DataFrame in a JSON file.

        Args:
            content (pd.DataFrame): The data to store.
            filename (str): The name of the JSON file (e.g. `corpus.json`).
        """
        self.__writer.write_to_json(content, filename)

    def read_data(self, filename: str) -> pd.DataFrame:
        """Load a DataFrame from a JSON file.

        Args:
            filename (str): The name of the JSON file (e.g. `corpus.json`).

        Returns:
            pd.DataFrame: The data contained in the file.

        Raises:
            FileNotFoundError: If the file does not exist in the storage directory.
        """
        return self.__reader.read_json(filename)
