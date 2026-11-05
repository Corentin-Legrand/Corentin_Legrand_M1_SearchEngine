"""Writing of DataFrames to JSON files in the storage directory."""

from pathlib import Path

import pandas as pd

from helpers.environment_manager import PROJECT_ROOT_PATH, EnvironmentManager
from service.interfaces.i_json_writer import IJsonWriter

STORAGE_DIR_KEY: str = "STORAGE_DIR"
JSON_ORIENT: str = "records"
JSON_DATE_FORMAT: str = "iso"
JSON_INDENT: int = 4


class JsonWriter(IJsonWriter):
    """
    Write DataFrames to JSON files located in the storage directory.

    Attributes:
        folder_path (Path): Directory where files are written (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the writer from the `STORAGE_DIR` environment variable.

        Raises:
            EnvironmentVariableNotFoundError: If `STORAGE_DIR` is not defined.
        """
        storage_dir: str = EnvironmentManager.get_instance().get_environment_variable(STORAGE_DIR_KEY)
        self.__folder_path: Path = PROJECT_ROOT_PATH / storage_dir

    def write_to_json(self, content: pd.DataFrame, filename: str) -> None:
        """Write a DataFrame to a JSON file, creating the storage directory if needed.

        Args:
            content (pd.DataFrame): The data to write, one JSON object per row.
            filename (str): The name of the file to write (e.g. `corpus.json`).
        """
        self.__folder_path.mkdir(parents=True, exist_ok=True)
        content.to_json(
            self.__folder_path / filename,
            orient=JSON_ORIENT,
            date_format=JSON_DATE_FORMAT,
            force_ascii=False,
            indent=JSON_INDENT,
        )
