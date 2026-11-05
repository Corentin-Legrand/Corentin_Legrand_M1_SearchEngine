"""Reading of JSON files from the storage directory into DataFrames."""

from pathlib import Path

import pandas as pd

from helpers.environment_manager import PROJECT_ROOT_PATH, EnvironmentManager
from service.interfaces.i_json_reader import IJsonReader

STORAGE_DIR_KEY: str = "STORAGE_DIR"
JSON_ORIENT: str = "records"


class JsonReader(IJsonReader):
    """
    Read JSON files located in the storage directory into DataFrames.

    Attributes:
        folder_path (Path): Directory where files are read from (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the reader from the `STORAGE_DIR` environment variable.

        Raises:
            EnvironmentVariableNotFoundError: If `STORAGE_DIR` is not defined.
        """
        storage_dir: str = EnvironmentManager.get_instance().get_environment_variable(STORAGE_DIR_KEY)
        self.__folder_path: Path = PROJECT_ROOT_PATH / storage_dir

    def read_json(self, filename: str) -> pd.DataFrame:
        """Read a JSON file into a DataFrame.

        Args:
            filename (str): The name of the file to read (e.g. `corpus.json`).

        Returns:
            pd.DataFrame: The data contained in the file, one row per JSON object.

        Raises:
            FileNotFoundError: If the file does not exist in the storage directory.
        """
        return pd.read_json(self.__folder_path / filename, orient=JSON_ORIENT)
