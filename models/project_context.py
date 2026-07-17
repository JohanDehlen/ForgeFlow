"""
ForgeBud

Project context model.

This dataclass represents the current state of a software
project. It is the primary object exchanged between
services and the user interface.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProjectContext:
    """
    Represents the current state of a project.
    """

    # -------------------------------------------------
    # Project
    # -------------------------------------------------

    project_path: str = ""

    # -------------------------------------------------
    # Git
    # -------------------------------------------------

    is_repository: bool = False

    branch: str = ""

    last_commit: str = ""

    changed_files: list[str] = field(default_factory=list)

    untracked_files: list[str] = field(default_factory=list)

    status: str = ""

    # -------------------------------------------------
    # Convenience
    # -------------------------------------------------

    @property
    def modified_count(self) -> int:
        """
        Number of modified tracked files.
        """
        return len(self.changed_files)

    @property
    def untracked_count(self) -> int:
        """
        Number of untracked files.
        """
        return len(self.untracked_files)

    @property
    def total_changes(self) -> int:
        """
        Total number of changed files.
        """
        return (
            self.modified_count +
            self.untracked_count
        )

    @property
    def is_clean(self) -> bool:
        """
        True if there are no changes.
        """
        return self.total_changes == 0