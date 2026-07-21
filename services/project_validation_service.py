"""
ForgeBud

Project validation service.

Performs read-only validation of ForgeBud project structure,
managed project-memory documents, and persistent project metadata.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models.project_info import ProjectInfo
from models.project_validation import ProjectValidation
from services.file_service import FileService


class ProjectValidationService:
    """
    Validates the health of a ForgeBud-managed project without
    modifying it.
    """

    FORGEBUD_FOLDER = ".forgebud"
    PROJECT_FILE = "project.json"

    REQUIRED_DOCUMENTS = (
        "project_summary.md",
        "roadmap.md",
        "architecture.md",
        "current_task.md",
        "assistant_rules.md",
        "coding_standards.md",
        "decisions.md",
        "changelog.md",
    )

    @classmethod
    def validate(
        cls,
        project_path: str | Path,
    ) -> ProjectValidation:
        """
        Validate a ForgeBud-managed project and return a health report.

        Validation is read-only and never changes the project.
        """
        result = ProjectValidation()
        project_root = Path(project_path)
        forgebud_folder = project_root / cls.FORGEBUD_FOLDER

        if not forgebud_folder.is_dir():
            result.add_error(
                "The project does not contain a .forgebud directory."
            )
            return result

        result.has_forgebud_directory = True

        cls._validate_required_documents(
            forgebud_folder,
            result,
        )
        cls._validate_project_metadata(
            forgebud_folder,
            result,
        )

        return result

    @classmethod
    def _validate_required_documents(
        cls,
        forgebud_folder: Path,
        result: ProjectValidation,
    ) -> None:
        """
        Validate documents created for every managed project.
        """
        for filename in cls.REQUIRED_DOCUMENTS:
            file_path = forgebud_folder / filename

            if FileService.exists(file_path):
                continue

            result.missing_files.append(filename)
            result.add_error(
                f"Required project-memory file is missing: {filename}"
            )

    @classmethod
    def _validate_project_metadata(
        cls,
        forgebud_folder: Path,
        result: ProjectValidation,
    ) -> None:
        """
        Validate project.json and its metadata fields.
        """
        project_file = forgebud_folder / cls.PROJECT_FILE

        if not FileService.exists(project_file):
            result.missing_files.append(cls.PROJECT_FILE)
            result.add_error(
                "Required project metadata file is missing: project.json"
            )
            return

        raw_text = FileService.read_text(project_file)

        if not raw_text.strip():
            result.add_error(
                "Project metadata file is empty or unreadable."
            )
            return

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as error:
            result.add_error(
                "Project metadata contains invalid JSON: "
                f"{error.msg} at line {error.lineno}, "
                f"column {error.colno}."
            )
            return

        if not isinstance(data, dict):
            result.add_error(
                "Project metadata must contain a JSON object."
            )
            return

        project_info = cls._create_project_info(data, result)

        if project_info is None:
            return

        result.has_project_metadata = True
        cls._validate_project_info(project_info, result)

    @staticmethod
    def _create_project_info(
        data: dict[str, Any],
        result: ProjectValidation,
    ) -> ProjectInfo | None:
        """
        Create ProjectInfo from decoded metadata.
        """
        try:
            return ProjectInfo(**data)
        except TypeError as error:
            result.add_error(
                "Project metadata does not match the expected "
                f"ProjectInfo structure: {error}"
            )
            return None

    @classmethod
    def _validate_project_info(
        cls,
        info: ProjectInfo,
        result: ProjectValidation,
    ) -> None:
        """
        Validate the fields stored in ProjectInfo.
        """
        string_fields = {
            "name": info.name,
            "version": info.version,
            "description": info.description,
            "language": info.language,
            "framework": info.framework,
            "repository": info.repository,
            "created_by": info.created_by,
            "forgebud_version": info.forgebud_version,
        }

        for field_name, value in string_fields.items():
            if isinstance(value, str):
                continue

            display_name = field_name.replace("_", " ")
            result.add_error(
                f"Project {display_name} must be a string."
            )

        if isinstance(info.name, str) and not info.name.strip():
            result.add_error("Project name is missing or blank.")

        if isinstance(info.version, str) and not info.version.strip():
            result.add_error("Project version is missing or blank.")

        cls._validate_optional_metadata(
            info,
            result,
        )
        cls._validate_assistant_rules(
            info,
            result,
        )

    @staticmethod
    def _validate_optional_metadata(
        info: ProjectInfo,
        result: ProjectValidation,
    ) -> None:
        """
        Record warnings for incomplete optional project metadata.
        """
        optional_fields = {
            "description": info.description,
            "language": info.language,
            "framework": info.framework,
        }

        for field_name, value in optional_fields.items():
            if not isinstance(value, str):
                continue

            if value.strip():
                continue

            display_name = field_name.capitalize()
            result.add_warning(
                f"Project {display_name} is blank."
            )

    @staticmethod
    def _validate_assistant_rules(
        info: ProjectInfo,
        result: ProjectValidation,
    ) -> None:
        """
        Validate persistent assistant-rule state.
        """
        if not isinstance(info.assistant_rules, list):
            result.add_error(
                "Project assistant rules must be a list of strings."
            )
            return

        for index, rule in enumerate(info.assistant_rules):
            if isinstance(rule, str):
                continue

            result.add_error(
                "Project assistant rule "
                f"{index + 1} must be a string."
            )