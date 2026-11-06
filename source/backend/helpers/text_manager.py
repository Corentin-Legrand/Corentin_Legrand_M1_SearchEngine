"""Simple measurements and cleaning on raw texts."""

MINIMUM_TEXT_LENGTH: int = 100
SENTENCE_SEPARATOR: str = "."
LINE_BREAK: str = "\n"
SPACE: str = " "


class TextManager:
    """
    Compute basic statistics on texts and clean them.
    Author: Corentin Legrand
    """

    def to_single_line(self, text: str) -> str:
        """Replace the line breaks of a text by spaces and trim it.

        Args:
            text (str): The raw text.

        Returns:
            str: The text on a single line.
        """
        return text.replace(LINE_BREAK, SPACE).strip()

    def join_texts(self, texts: list[str]) -> str:
        """Concatenate texts into a single string, one text per line.

        Each text is put on a single line first, so that the line breaks only separate the texts.

        Args:
            texts (list[str]): The texts to concatenate.

        Returns:
            str: The texts separated by `LINE_BREAK`.
        """
        return LINE_BREAK.join(self.to_single_line(text) for text in texts)

    def count_words(self, text: str) -> int:
        """Count the words of a text, words being separated by whitespace.

        Args:
            text (str): The text to analyse.

        Returns:
            int: The number of words.
        """
        return len(text.split())

    def count_sentences(self, text: str) -> int:
        """Count the sentences of a text, sentences being separated by dots.

        Blank fragments (e.g. after the final dot) are not counted.

        Args:
            text (str): The text to analyse.

        Returns:
            int: The number of sentences.
        """
        sentences: list[str] = text.split(SENTENCE_SEPARATOR)
        return len([sentence for sentence in sentences if sentence.strip()])

    def is_too_short(self, text: str) -> bool:
        """Tell whether a text is shorter than the minimum length (100 characters).

        Args:
            text (str): The text to check.

        Returns:
            bool: True if the text has strictly less than `MINIMUM_TEXT_LENGTH` characters.
        """
        return len(text) < MINIMUM_TEXT_LENGTH
