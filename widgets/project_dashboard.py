"""
ForgeBud

Project dashboard widget.

Displays the current project, repository, release, and project
validation information.
"""

from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from models.project_dashboard import ProjectDashboard
from models.project_validation import ProjectValidation


class ProjectDashboardWidget(QWidget):
    """
    Displays the current ProjectDashboard state.
    """

    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout(self)

        title_label = QLabel("Project Dashboard")
        main_layout.addWidget(title_label)

        self._create_project_section(main_layout)
        self._add_separator(main_layout)
        self._create_repository_section(main_layout)
        self._add_separator(main_layout)
        self._create_release_section(main_layout)
        self._add_separator(main_layout)
        self._create_validation_section(main_layout)

        main_layout.addStretch()

        self.clear()

    def _create_project_section(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the project information section.
        """
        form = QFormLayout()

        self.projectLabel = QLabel("-")
        self.descriptionLabel = QLabel("-")
        self.pathLabel = QLabel("-")
        self.initializationLabel = QLabel("-")

        self.descriptionLabel.setWordWrap(True)
        self.pathLabel.setWordWrap(True)

        form.addRow("Project", self.projectLabel)
        form.addRow("Description", self.descriptionLabel)
        form.addRow("Path", self.pathLabel)
        form.addRow("ForgeBud", self.initializationLabel)

        main_layout.addLayout(form)

    def _create_repository_section(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the repository information section.
        """
        form = QFormLayout()

        self.repositoryLabel = QLabel("-")
        self.branchLabel = QLabel("-")
        self.lastCommitLabel = QLabel("-")
        self.changedFilesLabel = QLabel("-")
        self.untrackedFilesLabel = QLabel("-")

        self.lastCommitLabel.setWordWrap(True)

        form.addRow("Repository", self.repositoryLabel)
        form.addRow("Branch", self.branchLabel)
        form.addRow("Last Commit", self.lastCommitLabel)
        form.addRow("Changed Files", self.changedFilesLabel)
        form.addRow("Untracked Files", self.untrackedFilesLabel)

        main_layout.addLayout(form)

    def _create_release_section(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the release information section.
        """
        form = QFormLayout()

        self.releaseVersionLabel = QLabel("-")
        self.releaseValidationLabel = QLabel("-")

        form.addRow("Release Version", self.releaseVersionLabel)
        form.addRow(
            "Release Validation",
            self.releaseValidationLabel,
        )

        main_layout.addLayout(form)

    def _create_validation_section(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the project-health validation section.
        """
        form = QFormLayout()

        self.projectHealthLabel = QLabel("-")
        self.validationSummaryLabel = QLabel("-")
        self.validationDetailsLabel = QLabel("-")

        self.validationSummaryLabel.setWordWrap(True)
        self.validationDetailsLabel.setWordWrap(True)

        form.addRow("Project Health", self.projectHealthLabel)
        form.addRow(
            "Validation Summary",
            self.validationSummaryLabel,
        )
        form.addRow(
            "Validation Details",
            self.validationDetailsLabel,
        )

        main_layout.addLayout(form)

    def _add_separator(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Add a horizontal separator to the dashboard.
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)

        main_layout.addWidget(separator)

    def set_dashboard(
        self,
        dashboard: ProjectDashboard,
    ) -> None:
        """
        Display the supplied project dashboard state.
        """
        project_info = dashboard.project_info
        project_context = dashboard.project_context
        release_manifest = dashboard.release_manifest

        self.projectLabel.setText(
            project_info.display_name or "-"
        )
        self.descriptionLabel.setText(
            project_info.description or "-"
        )
        self.pathLabel.setText(
            project_context.project_path or "-"
        )
        self.initializationLabel.setText(
            "Initialized"
            if dashboard.is_initialized
            else "Not initialized"
        )

        self.repositoryLabel.setText(
            "Git Repository"
            if project_context.is_repository
            else "Not a Git repository"
        )
        self.branchLabel.setText(
            project_context.branch or "-"
        )
        self.lastCommitLabel.setText(
            project_context.last_commit or "-"
        )
        self.changedFilesLabel.setText(
            str(project_context.modified_count)
        )
        self.untrackedFilesLabel.setText(
            str(project_context.untracked_count)
        )

        self.releaseVersionLabel.setText(
            release_manifest.version or "-"
        )
        self.releaseValidationLabel.setText(
            release_manifest.validation_status or "-"
        )

        self._set_project_validation(
            dashboard.project_validation,
            dashboard.is_initialized,
        )

    def clear(self) -> None:
        """
        Clear all displayed dashboard values.
        """
        self.projectLabel.setText("-")
        self.descriptionLabel.setText("-")
        self.pathLabel.setText("-")
        self.initializationLabel.setText("-")

        self.repositoryLabel.setText("-")
        self.branchLabel.setText("-")
        self.lastCommitLabel.setText("-")
        self.changedFilesLabel.setText("-")
        self.untrackedFilesLabel.setText("-")

        self.releaseVersionLabel.setText("-")
        self.releaseValidationLabel.setText("-")

        self.projectHealthLabel.setText("-")
        self.validationSummaryLabel.setText("-")
        self.validationDetailsLabel.setText("-")

    def _set_project_validation(
        self,
        validation: ProjectValidation,
        is_initialized: bool,
    ) -> None:
        """
        Display project-health validation results.
        """
        if not is_initialized:
            self.projectHealthLabel.setText("Not initialized")
            self.validationSummaryLabel.setText(
                "Project validation is unavailable until "
                "ForgeBud initialization is complete."
            )
            self.validationDetailsLabel.setText("-")
            return

        error_count = len(validation.errors)
        warning_count = len(validation.warnings)

        if validation.is_valid and not validation.has_warnings:
            self.projectHealthLabel.setText("Healthy")
            self.validationSummaryLabel.setText(
                "No project validation issues were found."
            )
            self.validationDetailsLabel.setText("-")
            return

        if validation.is_valid:
            self.projectHealthLabel.setText(
                "Healthy with warnings"
            )
        else:
            self.projectHealthLabel.setText("Issues detected")

        self.validationSummaryLabel.setText(
            f"{error_count} error(s), "
            f"{warning_count} warning(s)"
        )

        details = [
            *(f"Error: {message}" for message in validation.errors),
            *(
                f"Warning: {message}"
                for message in validation.warnings
            ),
        ]

        self.validationDetailsLabel.setText(
            "\n".join(details) if details else "-"
        )