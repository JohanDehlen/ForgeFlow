from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from version import APP_NAME, APP_VERSION

from widgets.project_panel import ProjectPanel
from widgets.status_bar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1200, 800)

        # -----------------------------------------
        # Central Widget
        # -----------------------------------------

        central = QWidget()
        self.setCentralWidget(central)

        mainLayout = QVBoxLayout(central)

        # -----------------------------------------
        # Main Content
        # -----------------------------------------

        contentLayout = QHBoxLayout()

        self.projectPanel = ProjectPanel()

        contentLayout.addWidget(self.projectPanel, 1)

        mainLayout.addLayout(contentLayout)

        # -----------------------------------------
        # Status Bar
        # -----------------------------------------

        self.statusBarWidget = StatusBar()

        mainLayout.addWidget(self.statusBarWidget)