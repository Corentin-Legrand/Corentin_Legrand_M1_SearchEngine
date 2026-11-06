"""Tests of the text helper."""

from helpers.text_manager import TextManager


def test_join_texts_puts_one_text_per_line() -> None:
    """The line breaks inside a text become spaces, so that a line is a text."""
    assert TextManager().join_texts(["first\ntext", " second "]) == "first text\nsecond"
