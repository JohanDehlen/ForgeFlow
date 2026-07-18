"""
ForgeBud

Decisions model.

Represents the persistent engineering decisions document stored in:

    .forgebud/decisions.md
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Decisions:
    """
    Persistent engineering decisions for a ForgeBud project.
    """

    markdown: str = ""

    @property
    def is_empty(self) -> bool:
        """
        Return True when the decisions document contains
        no meaningful text.
        """
        return not self.markdown.strip()