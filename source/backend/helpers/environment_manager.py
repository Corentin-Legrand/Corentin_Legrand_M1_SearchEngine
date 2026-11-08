"""Access to the application's environment variables."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT_DEPTH: int = 3
PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parents[PROJECT_ROOT_DEPTH]
ENV_FILE_PATH: Path = PROJECT_ROOT_PATH / ".env"
ENV_FILE_ENCODING: str = "utf-8"
COMMENT_PREFIX: str = "#"
KEY_VALUE_SEPARATOR: str = "="
QUOTE_CHARACTERS: tuple[str, ...] = ('"', "'")


class EnvironmentVariableNotFoundError(KeyError):
    """
    Raised when a requested environment variable is not defined.
    Author: Corentin Legrand
    """


class SingletonInstantiationError(RuntimeError):
    """
    Raised when a singleton is instantiated outside its accessor.
    Author: Corentin Legrand
    """


class EnvironmentManager:
    """
    Singleton giving access to the environment variables.
    Variables are read from the process environment first, then from the
    `.env` file located at the project root. The process environment takes
    precedence so that values injected by docker-compose override the file,
    which may be absent.

    Attributes:
        instance (EnvironmentManager | None): The unique instance (private, class scope).

    Author: Corentin Legrand
    """

    __instance: EnvironmentManager | None = None
    __CREATION_KEY: object = object()

    def __init__(self, creation_key: object) -> None:
        """Build the manager; use `get_instance` instead.

        Args:
            creation_key (object): Private key only known by `get_instance`.

        Raises:
            SingletonInstantiationError: If called outside `get_instance`.
        """
        if creation_key is not EnvironmentManager.__CREATION_KEY:
            raise SingletonInstantiationError(
                "EnvironmentManager is a singleton, use EnvironmentManager.get_instance()."
            )
        self.__file_variables: dict[str, str] = self.__read_env_file(ENV_FILE_PATH)

    @classmethod
    def get_instance(cls) -> EnvironmentManager:
        """Return the unique instance, creating it on first call.

        Returns:
            EnvironmentManager: The unique environment manager.
        """
        if cls.__instance is None:
            cls.__instance = cls(cls.__CREATION_KEY)
        return cls.__instance

    def get_environment_variable(self, key: str) -> str:
        """Return the value of an environment variable.

        Args:
            key (str): The name of the variable.

        Returns:
            str: The value from the process environment, or else from the `.env` file.

        Raises:
            EnvironmentVariableNotFoundError: If the variable is defined nowhere.
        """
        value: str | None = os.environ.get(key, self.__file_variables.get(key))
        if value is None:
            raise EnvironmentVariableNotFoundError(f"Environment variable '{key}' is not defined.")
        return value

    @staticmethod
    def __read_env_file(env_file_path: Path) -> dict[str, str]:
        """Parse a `.env` file made of `KEY=VALUE` lines.

        Empty lines, comment lines and lines without separator are ignored;
        surrounding quotes are removed from values.

        Args:
            env_file_path (Path): Path of the `.env` file.

        Returns:
            dict[str, str]: The variables found, empty if the file does not exist.
        """
        variables: dict[str, str] = {}
        if env_file_path.is_file():
            for raw_line in env_file_path.read_text(encoding=ENV_FILE_ENCODING).splitlines():
                line: str = raw_line.strip()
                if line and not line.startswith(COMMENT_PREFIX) and KEY_VALUE_SEPARATOR in line:
                    key, value = line.split(KEY_VALUE_SEPARATOR, 1)
                    variables[key.strip()] = EnvironmentManager.__unquote(value.strip())
        return variables

    @staticmethod
    def __unquote(value: str) -> str:
        """Remove matching surrounding quotes from a value.

        Args:
            value (str): The raw value.

        Returns:
            str: The value without its surrounding quotes.
        """
        is_quoted: bool = len(value) >= 2 and value[0] == value[-1] and value[0] in QUOTE_CHARACTERS
        return value[1:-1] if is_quoted else value
