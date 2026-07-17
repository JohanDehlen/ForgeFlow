from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from version import APP_NAME, APP_VERSION

from controllers.project_controller import ProjectController
from models.project_info import ProjectInfo
from widgets.project_panel import ProjectPanel
from widgets.status_bar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        mainLayout = QVBoxLayout(central)
        contentLayout = QHBoxLayout()

        self.projectPanel = ProjectPanel()
        contentLayout.addWidget(self.projectPanel)
        mainLayout.addLayout(contentLayout)

        self.statusBarWidget = StatusBar()
        mainLayout.addWidget(self.statusBarWidget)

        self.projectController = ProjectController(self)

        self.projectPanel.openButton.clicked.connect(
            self.projectController.open_project
        )
        self.projectPanel.initializeButton.clicked.connect(
            self.projectController.initialize_project
        )

    # ---------------- MainWindow façade ----------------

    def show_status(self, message: str) -> None:
        self.statusBarWidget.show_message(message)

    def select_project_folder(self) -> str:
        return QFileDialog.getExistingDirectory(
            self,
            "Open Project",
        )

    def show_information(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)

    def set_project(self, info: ProjectInfo) -> None:
        self.projectPanel.set_project(info)

    def clear_project(self) -> None:
        self.projectPanel.clear()

    def set_repository_status(self, text: str) -> None:
        self.projectPanel.set_repository_status(text)

    def enable_initialize(self) -> None:
        self.projectPanel.enable_initialize()

    def disable_initialize(self) -> None:
        self.projectPanel.disable_initialize()
