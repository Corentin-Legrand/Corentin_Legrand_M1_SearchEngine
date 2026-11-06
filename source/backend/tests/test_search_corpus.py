"""Tests of the interactive search script."""

from collections.abc import Callable, Iterator

import pytest

from models.corpus import Corpus
from script.search_corpus import NO_RESULT_MESSAGE, SearchCorpus
from service.search_engine import SearchEngine

TEXTS: list[str] = ["solar energy solar", "carbon energy", "carbon climate"]


def run_with_inputs(
    load_corpus: Callable[[list[str]], Corpus], monkeypatch: pytest.MonkeyPatch, inputs: list[str]
) -> None:
    """Run the script on a small corpus, the user typing the given lines.

    Args:
        load_corpus (Callable[[list[str]], Corpus]): Fixture filling the corpus.
        monkeypatch (pytest.MonkeyPatch): Fixture replacing `input`.
        inputs (list[str]): The lines typed by the user.
    """
    typed_lines: Iterator[str] = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed_lines))
    SearchCorpus(SearchEngine(load_corpus(TEXTS))).run()


def test_run_prints_best_document_title(
    load_corpus: Callable[[list[str]], Corpus], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The title of the matching document is printed."""
    run_with_inputs(load_corpus, monkeypatch, ["climate", ""])
    assert "title 2" in capsys.readouterr().out


def test_run_prints_message_without_result(
    load_corpus: Callable[[list[str]], Corpus], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A query matching nothing prints a message instead of an empty table."""
    run_with_inputs(load_corpus, monkeypatch, ["photovoltaic", ""])
    assert NO_RESULT_MESSAGE in capsys.readouterr().out


def test_run_survives_query_without_words(
    load_corpus: Callable[[list[str]], Corpus], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A query without words prints the error and lets the user search again."""
    run_with_inputs(load_corpus, monkeypatch, ["?!", "climate", ""])
    assert "title 2" in capsys.readouterr().out
