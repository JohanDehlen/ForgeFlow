from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.project_info import ProjectInfo
from services.prompt_template_service import PromptTemplateService


class ProjectPanel(QWidget):
    """
    Displays current-project information, project actions,
    prompt settings, and recent projects.
    """

    recentProjectSelected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout(self)

        self._create_project_information(main_layout)
        self._add_separator(main_layout)
        self._create_project_actions(main_layout)
        self._add_separator(main_layout)
        self._create_recent_projects(main_layout)

        main_layout.addStretch()

    def _create_project_information(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the current-project information display.
        """
        form = QFormLayout()

        self.nameLabel = QLabel("-")
        self.versionLabel = QLabel("-")
        self.languageLabel = QLabel("-")
        self.frameworkLabel = QLabel("-")
        self.repositoryLabel = QLabel("No Project Loaded")

        form.addRow("Project", self.nameLabel)
        form.addRow("Version", self.versionLabel)
        form.addRow("Language", self.languageLabel)
        form.addRow("Framework", self.frameworkLabel)
        form.addRow("Repository", self.repositoryLabel)

        main_layout.addLayout(form)

    def _create_project_actions(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create project and prompt action controls.
        """
        primary_button_layout = QHBoxLayout()

        self.openButton = QPushButton("Open Project")
        self.initializeButton = QPushButton(
            "Initialize ForgeBud"
        )
        self.initializeButton.setEnabled(False)

        primary_button_layout.addWidget(self.openButton)
        primary_button_layout.addWidget(
            self.initializeButton
        )

        main_layout.addLayout(primary_button_layout)

        prompt_form = QFormLayout()

        self.promptTemplateCombo = QComboBox()

        for template in PromptTemplateService.all():
            self.promptTemplateCombo.addItem(
                template.name,
                template.key,
            )

        prompt_form.addRow(
            "Prompt Template",
            self.promptTemplateCombo,
        )

        main_layout.addLayout(prompt_form)

        self.copyPromptButton = QPushButton(
            "Copy Engineering Prompt"
        )
        self.copyPromptButton.setEnabled(False)
        self.copyPromptButton.setToolTip(
            "Generate the current project's engineering prompt "
            "using the selected template and copy it to the "
            "clipboard."
        )

        main_layout.addWidget(self.copyPromptButton)

    def _create_recent_projects(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Create the recent-projects display.
        """
        recent_projects_label = QLabel("Recent Projects")
        main_layout.addWidget(recent_projects_label)

        self.recentProjectsList = QListWidget()
        self.recentProjectsList.setToolTip(
            "Select a project to open it."
        )
        self.recentProjectsList.itemClicked.connect(
            self._select_recent_project
        )

        main_layout.addWidget(self.recentProjectsList)

    def _add_separator(
        self,
        main_layout: QVBoxLayout,
    ) -> None:
        """
        Add a horizontal separator to the panel.
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)

        main_layout.addWidget(separator)

    def selected_prompt_template_key(self) -> str:
        """
        Return the selected prompt-template key.
        """
        template_key = self.promptTemplateCombo.currentData()

        if isinstance(template_key, str):
            return template_key

        return PromptTemplateService.DEFAULT_TEMPLATE_KEY

    def clear(self) -> None:
        """
        Clear the displayed current-project information.
        """
        self.nameLabel.setText("-")
        self.versionLabel.setText("-")
        self.languageLabel.setText("-")
        self.frameworkLabel.setText("-")
        self.repositoryLabel.setText("No Project Loaded")

        self.initializeButton.setEnabled(False)
        self.copyPromptButton.setEnabled(False)

    def set_project(self, info: ProjectInfo) -> None:
        """
        Display initialized project metadata.
        """
        self.nameLabel.setText(info.name or "-")
        self.versionLabel.setText(info.version or "-")
        self.languageLabel.setText(info.language or "-")
        self.frameworkLabel.setText(info.framework or "-")

        self.copyPromptButton.setEnabled(True)

    def set_repository_status(self, text: str) -> None:
        """
        Update repository status.
        """
        self.repositoryLabel.setText(text)

    def set_recent_projects(
        self,
        project_paths: list[str],
    ) -> None:
        """
        Display recent project folders.
        """
        self.recentProjectsList.clear()

        for project_path in project_paths:
            path = Path(project_path)
            item = QListWidgetItem(path.name or project_path)

            item.setData(
                Qt.ItemDataRole.UserRole,
                project_path,
            )
            item.setToolTip(project_path)

            self.recentProjectsList.addItem(item)

    def enable_initialize(self) -> None:
        """
        Enable the Initialize button.
        """
        self.initializeButton.setEnabled(True)

    def disable_initialize(self) -> None:
        """
        Disable the Initialize button.
        """
        self.initializeButton.setEnabled(False)

    def _select_recent_project(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Emit the full path for the selected recent project.
        """
        project_path = item.data(Qt.ItemDataRole.UserRole)

        if isinstance(project_path, str):
            self.recentProjectSelected.emit(project_path)