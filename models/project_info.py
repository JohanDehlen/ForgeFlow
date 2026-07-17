"""
ForgeBud

Project information model.

Represents the persistent project metadata stored in:

    .forgebud/project.json

This information changes infrequently and describes the
project itself rather than its current runtime state.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProjectInfo:
    """
    Persistent information describing a project.
    """

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    name: str = ""

    version: str = "0.1.0"

    description: str = ""

    # -------------------------------------------------
    # Technology
    # -------------------------------------------------

    language: str = ""

    framework: str = ""

    # -------------------------------------------------
    # Repository
    # -------------------------------------------------

    repository: str = ""

    # -------------------------------------------------
    # ForgeBud
    # -------------------------------------------------

    created_by: str = "ForgeBud"

    forgebud_version: str = "0.3.0"

    # -------------------------------------------------
    # AI Development Rules
    # -------------------------------------------------

    assistant_rules: list[str] = field(default_factory=list)

    # -------------------------------------------------
    # Convenience
    # -------------------------------------------------

    @property
    def display_name(self) -> str:
        """
        Display name used by the UI.
        """

        if self.version:
            return f"{self.name} v{self.version}"

        return self.name