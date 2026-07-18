from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from controllers.project_controller import ProjectController
from models.current_task import CurrentTask
from models.decisions import Decisions
from models.project_dashboard import ProjectDashboard
from models.project_info import ProjectInfo
from version import APP_NAME, APP_VERSION
from widgets.current_task_manager import (
    CurrentTaskManagerWidget,
)
from widgets.decisions_manager import DecisionsManagerWidget
from widgets.project_dashboard import ProjectDashboardWidget
from widgets.project_panel import ProjectPanel
from widgets.status_bar import StatusBar


class MainWindow(QMainWindow):
    """
    Owns the application UI and delegates project workflows
    to the project controller.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1200, 800)

        self._create_ui()
        self._create_controller()
        self._connect_signals()

        self.projectController.refresh_recent_projects()
        self.projectController.refresh_project_dashboard()
        self.projectController.refresh_current_task()
        self.projectController.refresh_decisions()

    def _create_ui(self) -> None:
        """
        Create and arrange the application widgets.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        content_layout = QHBoxLayout()

        self.projectPanel = ProjectPanel()
        content_layout.addWidget(self.projectPanel)

        workspace_layout = QVBoxLayout()

        self.projectDashboard = ProjectDashboardWidget()
        workspace_layout.addWidget(self.projectDashboard)

        project_memory_layout = QHBoxLayout()

        self.currentTaskManager = CurrentTaskManagerWidget()
        project_memory_layout.addWidget(
            self.currentTaskManager
        )

        self.decisionsManager = DecisionsManagerWidget()
        project_memory_layout.addWidget(
            self.decisionsManager
        )

        workspace_layout.addLayout(project_memory_layout)
        content_layout.addLayout(workspace_layout)

        main_layout.addLayout(content_layout)

        self.statusBarWidget = StatusBar()
        main_layout.addWidget(self.statusBarWidget)

    def _create_controller(self) -> None:
        """
        Create the controller that coordinates project workflows.
        """
        self.projectController = ProjectController(self)

    def _connect_signals(self) -> None:
        """
        Connect widget signals to controller actions.
        """
        self.projectPanel.openButton.clicked.connect(
            self.projectController.open_project
        )
        self.projectPanel.initializeButton.clicked.connect(
            self.projectController.initialize_project
        )
        self.projectPanel.recentProjectSelected.connect(
            self.projectController.open_recent_project
        )
        self.currentTaskManager.saveRequested.connect(
            self.projectController.save_current_task
        )
        self.decisionsManager.saveRequested.connect(
            self.projectController.save_decisions
        )

    def show_status(self, message: str) -> None:
        """
        Display an application status message.
        """
        self.statusBarWidget.show_message(message)

    def select_project_folder(self) -> str:
        """
        Ask the user to select a project folder.
        """
        return QFileDialog.getExistingDirectory(
            self,
            "Open Project",
        )

    def show_information(self, title: str, message: str) -> None:
        """
        Display an informational message dialog.
        """
        QMessageBox.information(self, title, message)

    def set_project(self, info: ProjectInfo) -> None:
        """
        Display loaded project metadata.
        """
        self.projectPanel.set_project(info)

    def clear_project(self) -> None:
        """
        Clear displayed project metadata.
        """
        self.projectPanel.clear()

    def set_repository_status(self, text: str) -> None:
        """
        Display the repository status.
        """
        self.projectPanel.set_repository_status(text)

    def set_project_dashboard(
        self,
        dashboard: ProjectDashboard,
    ) -> None:
        """
        Display current project dashboard state.
        """
        self.projectDashboard.set_dashboard(dashboard)

    def set_current_task(
        self,
        current_task: CurrentTask,
    ) -> None:
        """
        Display current-task state.
        """
        self.currentTaskManager.set_current_task(
            current_task
        )

    def clear_current_task(self) -> None:
        """
        Clear displayed current-task state.
        """
        self.currentTaskManager.clear()

    def enable_current_task_editing(self) -> None:
        """
        Enable current-task editing and saving.
        """
        self.currentTaskManager.enable_editing()

    def disable_current_task_editing(self) -> None:
        """
        Disable current-task editing and saving.
        """
        self.currentTaskManager.disable_editing()

    def set_decisions(
        self,
        decisions: Decisions,
    ) -> None:
        """
        Display engineering decisions state.
        """
        self.decisionsManager.set_decisions(decisions)

    def clear_decisions(self) -> None:
        """
        Clear displayed engineering decisions state.
        """
        self.decisionsManager.clear()

    def enable_decisions_editing(self) -> None:
        """
        Enable engineering decisions editing and saving.
        """
        self.decisionsManager.enable_editing()

    def disable_decisions_editing(self) -> None:
        """
        Disable engineering decisions editing and saving.
        """
        self.decisionsManager.disable_editing()

    def set_recent_projects(
        self,
        project_paths: list[str],
    ) -> None:
        """
        Display recent project folders.
        """
        self.projectPanel.set_recent_projects(project_paths)

    def enable_initialize(self) -> None:
        """
        Enable the project initialization action.
        """
        self.projectPanel.enable_initialize()

    def disable_initialize(self) -> None:
        """
        Disable the project initialization action.
        """
        self.projectPanel.disable_initialize()