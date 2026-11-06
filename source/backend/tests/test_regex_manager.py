"""Tests of the regular expression searches."""

import pandas as pd
import pytest

from helpers.regex_manager import ConcordanceColumn, InvalidContextSizeError, InvalidPatternError, RegexManager

TEXT: str = "Climate is changing. The weather is not the climate.\nA climatic study. Climate models improve."
CONTEXT_SIZE: int = 8


@pytest.fixture
def regex_manager() -> RegexManager:
    """Return the tested helper."""
    return RegexManager()


def test_find_passages_returns_sentences_holding_the_word(regex_manager: RegexManager) -> None:
    """The passages are the sentences holding the keyword, ignoring the case."""
    expected: list[str] = ["Climate is changing", "The weather is not the climate", "Climate models improve"]
    assert regex_manager.find_passages(TEXT, "climate") == expected


def test_find_passages_ignores_longer_words(regex_manager: RegexManager) -> None:
    """A word only matches as a whole word ("climatic" is not "climat")."""
    assert regex_manager.find_passages(TEXT, "climat") == []


def test_find_passages_takes_keyword_literally(regex_manager: RegexManager) -> None:
    """Regex special characters of the keyword are escaped ("3.5" does not match "345")."""
    assert regex_manager.find_passages("Costs are 3.5 times higher. Or 345.", "3.5") == ["Costs are 3.5 times higher"]


def test_find_passages_rejects_blank_keyword(regex_manager: RegexManager) -> None:
    """A blank keyword would match everything."""
    with pytest.raises(InvalidPatternError):
        regex_manager.find_passages(TEXT, "  ")


def test_find_concordances_has_expected_columns(regex_manager: RegexManager) -> None:
    """The concordance table has the left context, match and right context columns."""
    concordances: pd.DataFrame = regex_manager.find_concordances(TEXT, "climate", CONTEXT_SIZE)
    assert list(concordances.columns) == list(ConcordanceColumn)


def test_find_concordances_returns_one_row_per_occurrence(regex_manager: RegexManager) -> None:
    """Each occurrence of the expression gives one row."""
    assert len(regex_manager.find_concordances(TEXT, r"climat\w*", CONTEXT_SIZE)) == 4


def test_find_concordances_keeps_context_around_match(regex_manager: RegexManager) -> None:
    """The context is made of at most `context_size` characters on each side."""
    row: pd.Series = regex_manager.find_concordances("one two climate three four", "climate", CONTEXT_SIZE).iloc[0]
    assert (row[ConcordanceColumn.LEFT_CONTEXT], row[ConcordanceColumn.RIGHT_CONTEXT]) == ("one two ", " three f")


def test_find_concordances_cuts_context_at_document_boundary(regex_manager: RegexManager) -> None:
    """The context of an occurrence never comes from another document."""
    row: pd.Series = regex_manager.find_concordances("first doc\nclimate\nlast doc", "climate", CONTEXT_SIZE).iloc[0]
    assert (row[ConcordanceColumn.LEFT_CONTEXT], row[ConcordanceColumn.RIGHT_CONTEXT]) == ("", "")


def test_find_concordances_rejects_invalid_expression(regex_manager: RegexManager) -> None:
    """An invalid regular expression raises a dedicated error."""
    with pytest.raises(InvalidPatternError):
        regex_manager.find_concordances(TEXT, "(climate", CONTEXT_SIZE)


def test_find_concordances_rejects_negative_context_size(regex_manager: RegexManager) -> None:
    """The context size cannot be negative."""
    with pytest.raises(InvalidContextSizeError):
        regex_manager.find_concordances(TEXT, "climate", -1)
