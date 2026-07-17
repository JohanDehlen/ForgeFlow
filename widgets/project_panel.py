"""
ForgeFlow

Project selection panel.

Responsibilities:
- Display the currently selected project folder.
- Allow the user to browse for a project.
- Provide a clean public API for accessing the project path.
"""

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class ProjectPanel(QGroupBox):
    """
    Widget responsible for selecting and displaying
    the current project folder.
    """

    projectChanged = Signal(str)

    def __init__(self):
        super().__init__("Project")

        self._build_ui()

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        row = QHBoxLayout()

        self.pathEdit = QLineEdit()
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setPlaceholderText(
            "No project selected..."
        )

        self.browseButton = QPushButton("Browse...")

        row.addWidget(self.pathEdit)
        row.addWidget(self.browseButton)

        layout.addLayout(row)

        self.browseButton.clicked.connect(
            self._browse_project
        )

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def project_path(self) -> str:
        """
        Return the current project path.
        """

        return self.pathEdit.text()

    def set_project_path(self, path: str) -> None:
        """
        Set the current project path.
        """

        self.pathEdit.setText(path)

    # -------------------------------------------------
    # Private
    # -------------------------------------------------

    def _browse_project(self) -> None:

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder",
            self.project_path() or str(Path.home()),
        )

        if not folder:
            return

        self.set_project_path(folder)

        self.projectChanged.emit(folder)