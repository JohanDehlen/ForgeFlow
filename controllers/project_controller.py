from __future__ import annotations

from pathlib import Path
from typing import Protocol

from models.current_task import CurrentTask
from models.decisions import Decisions
from models.project_dashboard import ProjectDashboard
from models.project_info import ProjectInfo
from services.context_service import ContextService
from services.current_task_service import CurrentTaskService
from services.decisions_service import DecisionsService
from services.git_service import GitService
from services.project_service import ProjectService
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

    def show_information(self, title: str, message: str) -> None:
        """
        Display an informational message dialog.
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
    dashboard state, project-memory documents, and recent-project
    presentation.
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
        Load project, repository, dashboard, and project-memory
        information.
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
        self.refresh_current_task()
        self.refresh_decisions()

    def initialize_project(self) -> None:
        """
        Initialize the currently opened project for ForgeBud.
        """
        if self._project_path is None:
            self._window.show_information(
                "No Project",
                "Please open a project first.",
            )
            return

        ProjectService.initialize(
            self._project_path,
            self._create_project_info(),
        )

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
        self._window.show_status(
            "Engineering decisions saved successfully."
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
            project_info = ProjectService.load(
                self._project_path
            )

        dashboard = ProjectDashboard(
            project_info=project_info,
            project_context=ContextService.build(
                str(self._project_path)
            ),
            release_manifest=ReleaseManifestService.load(
                self._project_path
            ),
            is_initialized=is_initialized,
        )

        self._window.set_project_dashboard(dashboard)

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
        info = ProjectService.load(self._project_path)

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

        self._window.clear_current_task()
        self._window.disable_current_task_editing()

        self._window.clear_decisions()
        self._window.disable_decisions_editing()

        self._window.show_status(
            "Project ready for initialization."
        )

    def _create_project_info(self) -> ProjectInfo:
        """
        Create initial metadata for the current project.
        """
        return ProjectInfo(
            name=self._project_path.name,
            version="0.1.0",
            description="",
            language="Python",
            framework="Unknown",
        )