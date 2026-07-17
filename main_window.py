"""
ForgeFlow

Main application window.

Responsibilities:
- Create and arrange widgets.
- Connect widget signals.
- Coordinate application workflow.

Business logic belongs in services.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from version import (
    WINDOW_TITLE,
    APP_NAME,
    APP_DESCRIPTION,
)

from widgets.project_panel import ProjectPanel
from widgets.status_bar import StatusBar


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(1400, 900)

        self._build_ui()

    def _build_ui(self):
        """
        Construct the user interface.
        """

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        #
        # Header
        #

        title = QLabel(APP_NAME)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        subtitle = QLabel(APP_DESCRIPTION)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        #
        # Project Panel
        #

        self.projectPanel = ProjectPanel()
        layout.addWidget(self.projectPanel)

        #
        # Stretch
        #

        layout.addStretch()

        #
        # Status Bar
        #

        self.statusBarWidget = StatusBar()
        layout.addWidget(self.statusBarWidget)