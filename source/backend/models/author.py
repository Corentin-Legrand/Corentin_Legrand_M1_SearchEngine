"""Structure of an author of the corpus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.document import Document


@dataclass
class Author:
    """
    Author of documents.

    `production` is excluded from `repr` and comparisons because its documents point back to
    their author, which would otherwise loop forever.

    Attributes:
        name (str): Name of the author, unique in the corpus.
        nb_docs (int): Number of documents written by the author.
        production (dict[int, Document]): Documents written by the author, by document id.

    Author: Corentin Legrand
    """

    name: str
    nb_docs: int = 0
    production: dict[int, Document] = field(default_factory=dict, repr=False, compare=False)
