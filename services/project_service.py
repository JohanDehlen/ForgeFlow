"""
ForgeBud

Project service.

Responsible for creating and maintaining the
ForgeBud project metadata.

Project Structure

<Project>/
    .forgebud/
        project.json
        roadmap.md
        architecture.md
        current_task.md
        assistant_rules.md
        decisions.md
        changelog.md
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from models.project_info import ProjectInfo
from services.file_service import FileService


class ProjectService:

    FORGEBUD_FOLDER = ".forgebud"

    PROJECT_FILE = "project.json"

    DEFAULT_FILES = {
        "roadmap.md": "# Roadmap\n",
        "architecture.md": "# Architecture\n",
        "current_task.md": "# Current Task\n",
        "assistant_rules.md": "# Assistant Rules\n",
        "decisions.md": "# Decisions\n",
        "changelog.md": "# Changelog\n",
    }

    @classmethod
    def initialize(
        cls,
        project_path: str | Path,
        info: ProjectInfo,
    ) -> None:
        """
        Initialize a project for ForgeBud.
        """

        project_path = Path(project_path)

        fb_folder = project_path / cls.FORGEBUD_FOLDER

        FileService.create_directory(fb_folder)

        cls.save(project_path, info)

        for filename, contents in cls.DEFAULT_FILES.items():

            file = fb_folder / filename

            if not file.exists():
                FileService.write_text(
                    file,
                    contents,
                )

    @classmethod
    def save(
        cls,
        project_path: str | Path,
        info: ProjectInfo,
    ) -> None:
        """
        Save project.json.
        """

        project_path = Path(project_path)

        fb_folder = project_path / cls.FORGEBUD_FOLDER

        FileService.create_directory(fb_folder)

        project_file = fb_folder / cls.PROJECT_FILE

        project_file.write_text(
            json.dumps(
                asdict(info),
                indent=4,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(
        cls,
        project_path: str | Path,
    ) -> ProjectInfo:
        """
        Load project.json.
        """

        project_path = Path(project_path)

        project_file = (
            project_path
            / cls.FORGEBUD_FOLDER
            / cls.PROJECT_FILE
        )

        if not project_file.exists():
            return ProjectInfo()

        data = json.loads(
            project_file.read_text(
                encoding="utf-8"
            )
        )

        return ProjectInfo(**data)

    @classmethod
    def is_initialized(
        cls,
        project_path: str | Path,
    ) -> bool:
        """
        Returns True if the project has already
        been initialized for ForgeBud.
        """

        project_path = Path(project_path)

        return (
            project_path
            / cls.FORGEBUD_FOLDER
            / cls.PROJECT_FILE
        ).exists()