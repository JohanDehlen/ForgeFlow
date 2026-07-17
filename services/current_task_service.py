"""
ForgeBud

Current task service.

Responsible for loading, validating, and saving the current-task
document stored in a project's ForgeBud memory.
"""

from __future__ import annotations

from pathlib import Path

from models.current_task import CurrentTask
from services.file_service import FileService


class CurrentTaskService:
    """
    Manages persistent current-task data for a project.
    """

    FORGEBUD_FOLDER = ".forgebud"
    CURRENT_TASK_FILE = "current_task.md"

    @classmethod
    def load(
        cls,
        project_path: str | Path,
    ) -> CurrentTask:
        """
        Load a project's current-task document.

        Returns an empty CurrentTask when the document does not exist.
        """
        current_task_file = cls._current_task_path(project_path)

        if not current_task_file.exists():
            return CurrentTask()

        return CurrentTask(
            markdown=FileService.read_text(current_task_file)
        )

    @classmethod
    def save(
        cls,
        project_path: str | Path,
        current_task: CurrentTask,
    ) -> None:
        """
        Validate and save a project's current-task document.

        Raises ValueError when the current-task state is invalid.
        """
        errors = cls.validate(current_task)

        if errors:
            raise ValueError(
                "Current task cannot be saved: "
                + "; ".join(errors)
            )

        FileService.write_text(
            cls._current_task_path(project_path),
            cls._normalize_markdown(current_task.markdown),
        )

    @classmethod
    def validate(
        cls,
        current_task: CurrentTask,
    ) -> list[str]:
        """
        Return validation errors for current-task state.
        """
        if not isinstance(current_task, CurrentTask):
            return [
                "Current task must be a CurrentTask instance."
            ]

        if not isinstance(current_task.markdown, str):
            return [
                "Current task Markdown must be a string."
            ]

        return []

    @classmethod
    def _current_task_path(
        cls,
        project_path: str | Path,
    ) -> Path:
        """
        Return the current-task document path for a project.
        """
        return (
            Path(project_path)
            / cls.FORGEBUD_FOLDER
            / cls.CURRENT_TASK_FILE
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