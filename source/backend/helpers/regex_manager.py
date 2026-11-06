"""Regular expression searches on a text made of one document per line."""

import re
from enum import StrEnum

import pandas as pd

DOCUMENT_SEPARATOR: str = "\n"
# A passage is the sentence holding the keyword: it stops at a dot or at the end of the document.
# The lookbehind only lets a passage start at a sentence start, avoiding a quadratic backtracking.
PASSAGE_PATTERN: str = r"(?<![^.\n])[^.\n]*\b{keyword}\b[^.\n]*"
REGEX_FLAGS: re.RegexFlag = re.IGNORECASE


class ConcordanceColumn(StrEnum):
    """
    Columns of the concordance table.
    Author: Corentin Legrand
    """

    LEFT_CONTEXT = "left_context"
    MATCH = "match"
    RIGHT_CONTEXT = "right_context"


class InvalidPatternError(ValueError):
    """
    Raised when a searched keyword or expression is empty or is not a valid regular expression.
    Author: Corentin Legrand
    """


class InvalidContextSizeError(ValueError):
    """
    Raised when the context size of a concordance is negative.
    Author: Corentin Legrand
    """


class RegexManager:
    """
    Find passages and build concordances in a text holding one document per line.

    Searches ignore the case and never cross the boundary between two documents.

    Author: Corentin Legrand
    """

    def find_passages(self, text: str, keyword: str) -> list[str]:
        """Return the passages (sentences) holding a keyword as a whole word.

        Args:
            text (str): The text to search, one document per line.
            keyword (str): The word to search, taken literally.

        Returns:
            list[str]: The passages holding the keyword, in order of appearance.

        Raises:
            InvalidPatternError: If the keyword is blank.
        """
        if not keyword.strip():
            raise InvalidPatternError("The keyword to search is empty.")
        pattern: str = PASSAGE_PATTERN.format(keyword=re.escape(keyword.strip()))
        return [passage.strip() for passage in re.findall(pattern, text, REGEX_FLAGS)]

    def find_concordances(self, text: str, expression: str, context_size: int) -> pd.DataFrame:
        """Build the concordance of a regular expression.

        Each occurrence comes with the characters around it, cut at the document boundaries.

        Args:
            text (str): The text to search, one document per line.
            expression (str): The regular expression to search.
            context_size (int): The maximum number of characters kept on each side of an occurrence.

        Returns:
            pd.DataFrame: One row per occurrence, with `ConcordanceColumn` columns.

        Raises:
            InvalidPatternError: If the expression is empty or invalid.
            InvalidContextSizeError: If the context size is negative.
        """
        if context_size < 0:
            raise InvalidContextSizeError(f"The context size must be positive, got {context_size}.")
        rows: list[dict[str, str]] = [
            {
                ConcordanceColumn.LEFT_CONTEXT: self.__get_left_context(text, match.start(), context_size),
                ConcordanceColumn.MATCH: match.group(),
                ConcordanceColumn.RIGHT_CONTEXT: self.__get_right_context(text, match.end(), context_size),
            }
            for match in self.__compile(expression).finditer(text)
            if match.end() > match.start()
        ]
        return pd.DataFrame(rows, columns=list(ConcordanceColumn))

    @staticmethod
    def __compile(expression: str) -> re.Pattern[str]:
        """Compile a regular expression.

        Args:
            expression (str): The regular expression.

        Returns:
            re.Pattern[str]: The compiled expression, ignoring the case.

        Raises:
            InvalidPatternError: If the expression is empty or invalid.
        """
        if not expression:
            raise InvalidPatternError("The expression to search is empty.")
        try:
            return re.compile(expression, REGEX_FLAGS)
        except re.error as error:
            raise InvalidPatternError(f"Invalid regular expression '{expression}': {error}.") from error

    @staticmethod
    def __get_left_context(text: str, start: int, context_size: int) -> str:
        """Return the characters before an occurrence, within its document.

        Args:
            text (str): The searched text.
            start (int): The position where the occurrence starts.
            context_size (int): The maximum number of characters to return.

        Returns:
            str: The left context of the occurrence.
        """
        return text[max(0, start - context_size):start].rsplit(DOCUMENT_SEPARATOR, 1)[-1]

    @staticmethod
    def __get_right_context(text: str, end: int, context_size: int) -> str:
        """Return the characters after an occurrence, within its document.

        Args:
            text (str): The searched text.
            end (int): The position where the occurrence ends.
            context_size (int): The maximum number of characters to return.

        Returns:
            str: The right context of the occurrence.
        """
        return text[end:end + context_size].split(DOCUMENT_SEPARATOR, 1)[0]
