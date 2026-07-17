from __future__ import annotations

from pathlib import Path

from models.project_info import ProjectInfo

from services.git_service import GitService
from services.project_service import ProjectService


class ProjectController:
    """
    Coordinates project lifecycle operations.

    The controller owns no UI.

    It communicates only through the MainWindow façade.
    """

    def __init__(self, window):
        self._window = window
        self._project_path: Path | None = None

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def open_project(self) -> None:
        """
        Ask the user to select a project folder and load it.
        """

        folder = self._window.select_project_folder()

        if not folder:
            return

        self.load_project(folder)

    def load_project(self, folder: str | Path) -> None:
        """
        Load an existing project.
        """

        self._project_path = Path(folder)

        self._window.show_status(
            f"Opened project: {self._project_path.name}"
        )

        #
        # Git
        #

        if GitService.is_repository(self._project_path):

            branch = GitService.current_branch(
                self._project_path
            )

            self._window.set_repository_status(
                f"Git Repository ({branch})"
            )

        else:

            self._window.set_repository_status(
                "Not a Git repository"
            )

        #
        # ForgeBud
        #

        if ProjectService.is_initialized(
            self._project_path
        ):

            info = ProjectService.load(
                self._project_path
            )

            self._window.set_project(info)

            self._window.disable_initialize()

            self._window.show_status(
                "ForgeBud project loaded."
            )

        else:

            self._window.clear_project()

            self._window.set_repository_status(
                "Project not initialized"
            )

            self._window.enable_initialize()

            self._window.show_status(
                "Project ready for initialization."
            )

    def initialize_project(self) -> None:
        """
        Initialize the currently opened project.
        """

        if self._project_path is None:

            self._window.show_information(
                "No Project",
                "Please open a project first.",
            )

            return

        info = ProjectInfo()

        info.name = self._project_path.name
        info.version = "0.1.0"
        info.description = ""
        info.language = "Python"
        info.framework = "Unknown"

        ProjectService.initialize(
            self._project_path,
            info,
        )

        self.load_project(self._project_path)

        self._window.show_information(
            "ForgeBud",
            "Project initialized successfully.",
        )

        self._window.show_status(
            "Project initialized successfully."
        )