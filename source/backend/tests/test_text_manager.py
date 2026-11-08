"""Tests of the text helper."""

from helpers.text_manager import TextManager


def test_join_texts_puts_one_text_per_line() -> None:
    """The line breaks inside a text become spaces, so that a line is a text."""
    assert TextManager().join_texts(["first\ntext", " second "]) == "first text\nsecond"


def test_clean_text_lowers_and_removes_punctuation() -> None:
    """Case, line breaks, punctuation and extra spaces disappear; digits are kept."""
    assert TextManager().clean_text("Climate !\nCLIMATE, in 2026_ (really)?") == "climate climate in 2026 really"


def test_tokenize_splits_on_several_delimiters() -> None:
    """Spaces, tabs and punctuation all separate words."""
    assert TextManager().tokenize("solar\tenergy,wind  power.") == ["solar", "energy", "wind", "power"]
