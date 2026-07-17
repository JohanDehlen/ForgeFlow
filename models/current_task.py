"""
ForgeBud

Current task model.

Represents the persistent current-task document stored in:

    .forgebud/current_task.md
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CurrentTask:
    """
    Persistent current-task state for a ForgeBud project.
    """

    markdown: str = ""

    @property
    def is_empty(self) -> bool:
        """
        Return True when the task document contains no meaningful text.
        """
        return not self.markdown.strip()