from __future__ import annotations

from pathlib import Path
from typing import Protocol

from models.coding_standards import CodingStandards
from models.current_task import CurrentTask
from models.decisions import Decisions
from models.project_dashboard import ProjectDashboard
from models.project_info import ProjectInfo
from models.project_summary import ProjectSummary
from services.clipboard_export_service import (
    ClipboardExportService,
)
from services.coding_standards_service import (
    CodingStandardsService,
)
from services.context_service import ContextService
from services.current_task_service import CurrentTaskService
from services.decisions_service import DecisionsService
from services.engineering_context_service import (
    EngineeringContextService,
)
from services.git_service import GitService
from services.project_service import ProjectService
from services.project_summary_service import (
    ProjectSummaryService,
)
from services.project_validation_service import (
    ProjectValidationService,
)
from services.prompt_builder_service import PromptBuilderService
from services.release_manifest_service import (
    ReleaseManifestService,
)
from services.settings_service import SettingsService


class ProjectWindow(Protocol):
    """
    Defines the UI operations required by ProjectController.
    """

    def show_status(self, message: str) -> None:
        """
        Display an application status message.
        """

    def select_project_folder(self) -> str:
        """
        Ask the user to select a project folder.
        """

    def request_project_initialization(
        self,
        project_info: ProjectInfo,
    ) -> ProjectInfo | None:
        """
        Display the project initialization form.

        Return confirmed project information or None when canceled.
        """

    def show_information(
        self,
        title: str,
        message: str,
    ) -> None:
        """
        Display an informational message dialog.
        """

    def selected_prompt_template_key(self) -> str:
        """
        Return the selected prompt-template key.
        """

    def set_project(self, info: ProjectInfo) -> None:
        """
        Display project metadata.
        """

    def clear_project(self) -> None:
        """
        Clear displayed project metadata.
        """

    def set_repository_status(self, text: str) -> None:
        """
        Display the repository status.
        """

    def set_project_dashboard(
        self,
        dashboard: ProjectDashboard,
    ) -> None:
        """
        Display project dashboard state.
        """

    def set_project_summary(
        self,
        project_summary: ProjectSummary,
    ) -> None:
        """
        Display project-summary state.
        """

    def clear_project_summary(self) -> None:
        """
        Clear displayed project-summary state.
        """

    def enable_project_summary_editing(self) -> None:
        """
        Enable project-summary editing and saving.
        """

    def disable_project_summary_editing(self) -> None:
        """
        Disable project-summary editing and saving.
        """

    def set_current_task(
        self,
        current_task: CurrentTask,
    ) -> None:
        """
        Display current-task state.
        """

    def clear_current_task(self) -> None:
        """
        Clear displayed current-task state.
        """

    def enable_current_task_editing(self) -> None:
        """
        Enable current-task editing and saving.
        """

    def disable_current_task_editing(self) -> None:
        """
        Disable current-task editing and saving.
        """

    def set_decisions(
        self,
        decisions: Decisions,
    ) -> None:
        """
        Display engineering decisions state.
        """

    def clear_decisions(self) -> None:
        """
        Clear displayed engineering decisions state.
        """

    def enable_decisions_editing(self) -> None:
        """
        Enable engineering decisions editing and saving.
        """

    def disable_decisions_editing(self) -> None:
        """
        Disable engineering decisions editing and saving.
        """

    def set_coding_standards(
        self,
        coding_standards: CodingStandards,
    ) -> None:
        """
        Display coding-standards state.
        """

    def clear_coding_standards(self) -> None:
        """
        Clear displayed coding-standards state.
        """

    def enable_coding_standards_editing(self) -> None:
        """
        Enable coding-standards editing and saving.
        """

    def disable_coding_standards_editing(self) -> None:
        """
        Disable coding-standards editing and saving.
        """

    def enable_initialize(self) -> None:
        """
        Enable project initialization.
        """

    def disable_initialize(self) -> None:
        """
        Disable project initialization.
        """

    def set_recent_projects(
        self,
        project_paths: list[str],
    ) -> None:
        """
        Display recent project folders.
        """


class ProjectController:
    """
    Coordinates project selection, loading, initialization,
    dashboard state, project validation, project-memory documents,
    prompt export, and recent-project presentation.
    """

    def __init__(self, window: ProjectWindow) -> None:
        self._window = window
        self._project_path: Path | None = None

    def open_project(self) -> None:
        """
        Ask the user to select and load a project folder.
        """
        folder = self._window.select_project_folder()

        if not folder:
            return

        self.load_project(folder)

    def open_recent_project(self, folder: str) -> None:
        """
        Load a project selected from the recent-projects list.
        """
        if not Path(folder).is_dir():
            self.refresh_recent_projects()
            return

        self.load_project(folder)

    def load_project(self, folder: str | Path) -> None:
        """
        Load project, repository, dashboard, validation, and
        project-memory information.
        """
        project_path = Path(folder)

        if not project_path.is_dir():
            return

        self._project_path = project_path
        SettingsService.add_recent_project(self._project_path)
        self.refresh_recent_projects()

        self._window.show_status(
            f"Opened project: {self._project_path.name}"
        )
        self._update_repository_status()

        if ProjectService.is_initialized(self._project_path):
            self._load_initialized_project()
        else:
            self._show_uninitialized_project()

        self.refresh_project_dashboard()
        self.refresh_project_summary()
        self.refresh_current_task()
        self.refresh_decisions()
        self.refresh_coding_standards()

    def initialize_project(self) -> None:
        """
        Collect metadata and initialize the currently opened project.
        """
        if self._project_path is None:
            self._window.show_information(
                "No Project",
                "Please open a project first.",
            )
            return

        initial_info = self._create_project_info()
        confirmed_info = (
            self._window.request_project_initialization(
                initial_info
            )
        )

        if confirmed_info is None:
            self._window.show_status(
                "Project initialization canceled."
            )
            return

        try:
            ProjectService.initialize(
                self._project_path,
                confirmed_info,
            )
        except ValueError as error:
            self._window.show_information(
                "Project Initialization",
                str(error),
            )
            self._window.show_status(
                "Project initialization failed."
            )
            return

        SettingsService.add_recent_project(self._project_path)
        self.refresh_recent_projects()
        self.load_project(self._project_path)

        self._window.show_information(
            "ForgeBud",
            "Project initialized successfully.",
        )
        self._window.show_status(
            "Project initialized successfully."
        )

    def export_prompt_to_clipboard(self) -> None:
        """
        Build and copy the current project's engineering prompt.
        """
        if self._project_path is None:
            self._window.show_information(
                "No Project",
                "Please open a project first.",
            )
            return

        if not ProjectService.is_initialized(
            self._project_path
        ):
            self._window.show_information(
                "Project Not Initialized",
                "Initialize the project before copying its prompt.",
            )
            self._window.show_status(
                "Prompt could not be copied."
            )
            return

        template_key = (
            self._window.selected_prompt_template_key()
        )

        try:
            context = EngineeringContextService.build(
                self._project_path
            )
            prompt = PromptBuilderService.build(
                context,
                template_key,
            )
            result = ClipboardExportService.export(prompt)
        except (
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
        ) as error:
            self._window.show_information(
                "Copy Engineering Prompt",
                str(error),
            )
            self._window.show_status(
                "Prompt could not be copied."
            )
            return

        if not result.success:
            self._window.show_information(
                "Copy Engineering Prompt",
                result.message or "Prompt export failed.",
            )
            self._window.show_status(
                "Prompt could not be copied."
            )
            return

        self._window.show_status(
            f"{result.message} "
            f"({prompt.token_estimate} estimated tokens)"
        )

    def save_project_summary(self, markdown: str) -> None:
        """
        Save project-summary Markdown for the opened project.
        """
        if not self._can_save_project_document(
            "its project summary"
        ):
            return

        project_summary = ProjectSummary(markdown=markdown)

        try:
            ProjectSummaryService.save(
                self._project_path,
                project_summary,
            )
        except ValueError as error:
            self._window.show_information(
                "Project Summary",
                str(error),
            )
            self._window.show_status(
                "Project summary could not be saved."
            )
            return

        self.refresh_project_summary()
        self.refresh_project_dashboard()
        self._window.show_status(
            "Project summary saved successfully."
        )

    def save_current_task(self, markdown: str) -> None:
        """
        Save current-task Markdown for the opened project.
        """
        if not self._can_save_project_document(
            "its current task"
        ):
            return

        current_task = CurrentTask(markdown=markdown)

        try:
            CurrentTaskService.save(
                self._project_path,
                current_task,
            )
        except ValueError as error:
            self._window.show_information(
                "Current Task",
                str(error),
            )
            self._window.show_status(
                "Current task could not be saved."
            )
            return

        self.refresh_current_task()
        self.refresh_project_dashboard()
        self._window.show_status(
            "Current task saved successfully."
        )

    def save_decisions(self, markdown: str) -> None:
        """
        Save engineering decisions Markdown for the opened project.
        """
        if not self._can_save_project_document(
            "its engineering decisions"
        ):
            return

        decisions = Decisions(markdown=markdown)

        try:
            DecisionsService.save(
                self._project_path,
                decisions,
            )
        except ValueError as error:
            self._window.show_information(
                "Engineering Decisions",
                str(error),
            )
            self._window.show_status(
                "Engineering decisions could not be saved."
            )
            return

        self.refresh_decisions()
        self.refresh_project_dashboard()
        self._window.show_status(
            "Engineering decisions saved successfully."
        )

    def save_coding_standards(self, markdown: str) -> None:
        """
        Save coding-standards Markdown for the opened project.
        """
        if not self._can_save_project_document(
            "its coding standards"
        ):
            return

        coding_standards = CodingStandards(
            markdown=markdown
        )

        try:
            CodingStandardsService.save(
                self._project_path,
                coding_standards,
            )
        except ValueError as error:
            self._window.show_information(
                "Coding Standards",
                str(error),
            )
            self._window.show_status(
                "Coding standards could not be saved."
            )
            return

        self.refresh_coding_standards()
        self.refresh_project_dashboard()
        self._window.show_status(
            "Coding standards saved successfully."
        )

    def refresh_recent_projects(self) -> None:
        """
        Load valid recent projects and display them through the UI.
        """
        self._window.set_recent_projects(
            SettingsService.get_recent_projects()
        )

    def refresh_project_dashboard(self) -> None:
        """
        Build and display the current project dashboard state.
        """
        if self._project_path is None:
            self._window.set_project_dashboard(
                ProjectDashboard()
            )
            return

        is_initialized = ProjectService.is_initialized(
            self._project_path
        )

        project_info = ProjectInfo()

        if is_initialized:
            try:
                project_info = ProjectService.load(
                    self._project_path
                )
            except (TypeError, ValueError):
                project_info = ProjectInfo()

        dashboard = ProjectDashboard(
            project_info=project_info,
            project_context=ContextService.build(
                str(self._project_path)
            ),
            release_manifest=ReleaseManifestService.load(
                self._project_path
            ),
            project_validation=(
                ProjectValidationService.validate(
                    self._project_path
                )
            ),
            is_initialized=is_initialized,
        )

        self._window.set_project_dashboard(dashboard)

    def refresh_project_summary(self) -> None:
        """
        Load and display project-summary state for the opened project.
        """
        if not self._has_initialized_project():
            self._window.clear_project_summary()
            self._window.disable_project_summary_editing()
            return

        project_summary = ProjectSummaryService.load(
            self._project_path
        )

        self._window.set_project_summary(project_summary)
        self._window.enable_project_summary_editing()

    def refresh_current_task(self) -> None:
        """
        Load and display current-task state for the opened project.
        """
        if not self._has_initialized_project():
            self._window.clear_current_task()
            self._window.disable_current_task_editing()
            return

        current_task = CurrentTaskService.load(
            self._project_path
        )

        self._window.set_current_task(current_task)
        self._window.enable_current_task_editing()

    def refresh_decisions(self) -> None:
        """
        Load and display engineering decisions for the opened project.
        """
        if not self._has_initialized_project():
            self._window.clear_decisions()
            self._window.disable_decisions_editing()
            return

        decisions = DecisionsService.load(
            self._project_path
        )

        self._window.set_decisions(decisions)
        self._window.enable_decisions_editing()

    def refresh_coding_standards(self) -> None:
        """
        Load and display coding standards for the opened project.
        """
        if not self._has_initialized_project():
            self._window.clear_coding_standards()
            self._window.disable_coding_standards_editing()
            return

        coding_standards = CodingStandardsService.load(
            self._project_path
        )

        self._window.set_coding_standards(
            coding_standards
        )
        self._window.enable_coding_standards_editing()

    def _can_save_project_document(
        self,
        document_description: str,
    ) -> bool:
        """
        Return whether a project-memory document may be saved.
        """
        if self._project_path is None:
            self._window.show_information(
                "No Project",
                "Please open a project first.",
            )
            return False

        if not ProjectService.is_initialized(
            self._project_path
        ):
            self._window.show_information(
                "Project Not Initialized",
                "Initialize the project before saving "
                f"{document_description}.",
            )
            return False

        return True

    def _has_initialized_project(self) -> bool:
        """
        Return whether an initialized project is currently open.
        """
        return (
            self._project_path is not None
            and ProjectService.is_initialized(
                self._project_path
            )
        )

    def _update_repository_status(self) -> None:
        """
        Load and display the current Git repository status.
        """
        if not GitService.is_repository(self._project_path):
            self._window.set_repository_status(
                "Not a Git repository"
            )
            return

        branch = GitService.current_branch(
            self._project_path
        )

        self._window.set_repository_status(
            f"Git Repository ({branch})"
        )

    def _load_initialized_project(self) -> None:
        """
        Load metadata for an initialized ForgeBud project.
        """
        try:
            info = ProjectService.load(self._project_path)
        except (TypeError, ValueError):
            self._window.clear_project()
            self._window.disable_initialize()
            self._window.show_status(
                "ForgeBud project metadata could not be loaded."
            )
            return

        self._window.set_project(info)
        self._window.disable_initialize()
        self._window.show_status("ForgeBud project loaded.")

    def _show_uninitialized_project(self) -> None:
        """
        Display the state of a project that is not initialized.
        """
        self._window.clear_project()
        self._window.set_repository_status(
            "Project not initialized"
        )
        self._window.enable_initialize()

        self._window.clear_project_summary()
        self._window.disable_project_summary_editing()

        self._window.clear_current_task()
        self._window.disable_current_task_editing()

        self._window.clear_decisions()
        self._window.disable_decisions_editing()

        self._window.clear_coding_standards()
        self._window.disable_coding_standards_editing()

        self._window.show_status(
            "Project ready for initialization."
        )

    def _create_project_info(self) -> ProjectInfo:
        """
        Create initial metadata for the initialization form.
        """
        repository = ""

        if GitService.is_repository(self._project_path):
            repository = str(self._project_path.resolve())

        return ProjectInfo(
            name=self._project_path.name,
            version="0.1.0",
            description="",
            language="",
            framework="",
            repository=repository,
        )