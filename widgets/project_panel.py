from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
)

from models.project_info import ProjectInfo


class ProjectPanel(QWidget):
    """
    Displays information about the currently
    opened project.
    """

    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)

        # -------------------------------------
        # Project Information
        # -------------------------------------

        form = QFormLayout()

        self.nameLabel = QLabel("-")
        self.versionLabel = QLabel("-")
        self.languageLabel = QLabel("-")
        self.frameworkLabel = QLabel("-")
        self.repositoryLabel = QLabel("Not Loaded")

        form.addRow("Project", self.nameLabel)
        form.addRow("Version", self.versionLabel)
        form.addRow("Language", self.languageLabel)
        form.addRow("Framework", self.frameworkLabel)
        form.addRow("Repository", self.repositoryLabel)

        mainLayout.addLayout(form)

        # -------------------------------------
        # Separator
        # -------------------------------------

        line = QFrame()
        line.setFrameShape(QFrame.HLine)

        mainLayout.addWidget(line)

        # -------------------------------------
        # Buttons
        # -------------------------------------

        buttonLayout = QHBoxLayout()

        self.openButton = QPushButton("Open Project")
        self.initializeButton = QPushButton("Initialize ForgeBud")

        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.initializeButton)

        mainLayout.addLayout(buttonLayout)

        mainLayout.addStretch()

    def clear(self):
        """
        Clears the displayed project information.
        """

        self.nameLabel.setText("-")
        self.versionLabel.setText("-")
        self.languageLabel.setText("-")
        self.frameworkLabel.setText("-")
        self.repositoryLabel.setText("Not Loaded")

    def set_project(self, info: ProjectInfo):
        """
        Displays project information.
        """

        self.nameLabel.setText(info.name or "-")
        self.versionLabel.setText(info.version or "-")
        self.languageLabel.setText(info.language or "-")
        self.frameworkLabel.setText(info.framework or "-")

    def set_repository_status(self, status: str):
        """
        Updates the repository status.
        """

        self.repositoryLabel.setText(status)