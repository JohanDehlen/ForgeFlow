"""
ForgeBud

Decisions service.

Responsible for loading, validating, and saving the engineering
decisions document stored in a project's ForgeBud memory.
"""

from __future__ import annotations

from pathlib import Path

from models.decisions import Decisions
from services.file_service import FileService


class DecisionsService:
    """
    Manages persistent engineering decisions for a project.
    """

    FORGEBUD_FOLDER = ".forgebud"
    DECISIONS_FILE = "decisions.md"

    @classmethod
    def load(
        cls,
        project_path: str | Path,
    ) -> Decisions:
        """
        Load a project's engineering decisions document.

        Returns empty Decisions state when the document does not exist.
        """
        decisions_file = cls._decisions_path(project_path)

        if not decisions_file.exists():
            return Decisions()

        return Decisions(
            markdown=FileService.read_text(decisions_file)
        )

    @classmethod
    def save(
        cls,
        project_path: str | Path,
        decisions: Decisions,
    ) -> None:
        """
        Validate and save a project's engineering decisions.

        Raises ValueError when the decisions state is invalid.
        """
        errors = cls.validate(decisions)

        if errors:
            raise ValueError(
                "Decisions cannot be saved: "
                + "; ".join(errors)
            )

        FileService.write_text(
            cls._decisions_path(project_path),
            cls._normalize_markdown(decisions.markdown),
        )

    @classmethod
    def validate(
        cls,
        decisions: Decisions,
    ) -> list[str]:
        """
        Return validation errors for decisions state.
        """
        if not isinstance(decisions, Decisions):
            return [
                "Decisions must be a Decisions instance."
            ]

        if not isinstance(decisions.markdown, str):
            return [
                "Decisions Markdown must be a string."
            ]

        return []

    @classmethod
    def _decisions_path(
        cls,
        project_path: str | Path,
    ) -> Path:
        """
        Return the engineering decisions document path.
        """
        return (
            Path(project_path)
            / cls.FORGEBUD_FOLDER
            / cls.DECISIONS_FILE
        )

    @staticmethod
    def _normalize_markdown(markdown: str) -> str:
        """
        Normalize Markdown before it is written to disk.
        """
        normalized = markdown.rstrip()

        if not normalized:
            return ""

        return normalized + "\n"