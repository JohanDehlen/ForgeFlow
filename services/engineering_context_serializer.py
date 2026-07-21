"""
ForgeBud

Engineering Context serializer.

Converts an EngineeringContext into a deterministic Markdown
document suitable for AI systems and other engineering consumers.
"""

from __future__ import annotations

from models.engineering_context import EngineeringContext


class EngineeringContextSerializer:
    """
    Serializes EngineeringContext into Markdown.
    """

    @classmethod
    def to_markdown(
        cls,
        context: EngineeringContext,
    ) -> str:
        """
        Convert EngineeringContext into structured Markdown.
        """
        sections: list[str] = []

        cls._append_project_information(sections, context)

        cls._append_markdown_section(
            sections,
            "Project Summary",
            context.project_summary.markdown,
        )
        cls._append_markdown_section(
            sections,
            "Current Task",
            context.current_task.markdown,
        )
        cls._append_markdown_section(
            sections,
            "Coding Standards",
            context.coding_standards.markdown,
        )
        cls._append_markdown_section(
            sections,
            "Engineering Decisions",
            context.decisions.markdown,
        )

        cls._append_release_manifest(sections, context)
        cls._append_repository_context(sections, context)
        cls._append_project_validation(sections, context)

        return "\n".join(sections).strip() + "\n"

    @staticmethod
    def _append_project_information(
        sections: list[str],
        context: EngineeringContext,
    ) -> None:
        """
        Append project metadata.
        """
        project_info = context.project_info

        sections.extend(
            [
                "# Project Information",
                "",
                f"Name: {project_info.name}",
                f"Version: {project_info.version}",
                f"Description: {project_info.description}",
                f"Language: {project_info.language}",
                f"Framework: {project_info.framework}",
                f"Repository: {project_info.repository}",
            ]
        )

    @classmethod
    def _append_markdown_section(
        cls,
        sections: list[str],
        title: str,
        markdown: str,
    ) -> None:
        """
        Append a stored Markdown document without duplicating its
        leading document title.
        """
        normalized_markdown = cls._remove_leading_heading(
            markdown
        )

        sections.extend(
            [
                "",
                f"# {title}",
                "",
                normalized_markdown or "No information recorded.",
            ]
        )

    @staticmethod
    def _remove_leading_heading(markdown: str) -> str:
        """
        Remove one leading level-one Markdown heading.

        Project-memory documents normally contain their own document
        title. The serializer supplies canonical section headings, so
        the stored leading heading is omitted from generated context.
        """
        lines = markdown.strip().splitlines()

        while lines and not lines[0].strip():
            lines.pop(0)

        if lines and lines[0].strip().startswith("# "):
            lines.pop(0)

        while lines and not lines[0].strip():
            lines.pop(0)

        return "\n".join(lines).strip()

    @staticmethod
    def _append_release_manifest(
        sections: list[str],
        context: EngineeringContext,
    ) -> None:
        """
        Append structured release-manifest state.
        """
        manifest = context.release_manifest

        sections.extend(
            [
                "",
                "# Release Manifest",
                "",
                f"Version: {manifest.version or '-'}",
                f"Goal: {manifest.goal or '-'}",
                (
                    "Validation Status: "
                    f"{manifest.validation_status or '-'}"
                ),
            ]
        )

        if manifest.files_added:
            sections.extend(["", "Files Added:"])
            sections.extend(
                f"- {path}" for path in manifest.files_added
            )

        if manifest.files_changed:
            sections.extend(["", "Files Changed:"])
            sections.extend(
                f"- {path}" for path in manifest.files_changed
            )

        if manifest.files_removed:
            sections.extend(["", "Files Removed:"])
            sections.extend(
                f"- {path}" for path in manifest.files_removed
            )

        if manifest.validation_details:
            sections.extend(["", "Validation Details:"])
            sections.extend(
                f"- {detail}"
                for detail in manifest.validation_details
            )

        if manifest.known_issues:
            sections.extend(["", "Known Issues:"])
            sections.extend(
                f"- {issue}" for issue in manifest.known_issues
            )

        if manifest.release_notes:
            sections.extend(["", "Release Notes:"])
            sections.extend(
                f"- {note}" for note in manifest.release_notes
            )

        if manifest.future_work:
            sections.extend(["", "Future Work:"])
            sections.extend(
                f"- {item}" for item in manifest.future_work
            )

    @staticmethod
    def _append_repository_context(
        sections: list[str],
        context: EngineeringContext,
    ) -> None:
        """
        Append repository state.
        """
        project_context = context.project_context

        sections.extend(
            [
                "",
                "# Repository",
                "",
                f"Path: {project_context.project_path or '-'}",
                (
                    "Git Repository: "
                    f"{project_context.is_repository}"
                ),
                f"Branch: {project_context.branch or '-'}",
                (
                    "Last Commit: "
                    f"{project_context.last_commit or '-'}"
                ),
                (
                    "Modified Files: "
                    f"{project_context.modified_count}"
                ),
                (
                    "Untracked Files: "
                    f"{project_context.untracked_count}"
                ),
            ]
        )

    @staticmethod
    def _append_project_validation(
        sections: list[str],
        context: EngineeringContext,
    ) -> None:
        """
        Append project-validation state.
        """
        validation = context.project_validation

        sections.extend(
            [
                "",
                "# Project Validation",
                "",
                f"Valid: {validation.is_valid}",
                (
                    "ForgeBud Directory Present: "
                    f"{validation.has_forgebud_directory}"
                ),
                (
                    "Project Metadata Present: "
                    f"{validation.has_project_metadata}"
                ),
            ]
        )

        if validation.missing_files:
            sections.extend(["", "Missing Files:"])
            sections.extend(
                f"- {filename}"
                for filename in validation.missing_files
            )

        if validation.errors:
            sections.extend(["", "Errors:"])
            sections.extend(
                f"- {error}" for error in validation.errors
            )

        if validation.warnings:
            sections.extend(["", "Warnings:"])
            sections.extend(
                f"- {warning}" for warning in validation.warnings
            )