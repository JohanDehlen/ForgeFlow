"""
ForgeFlow

Application entry point.

Responsibilities:
- Create the QApplication.
- Create and display the MainWindow.
- Start the Qt event loop.
"""

import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from version import APP_NAME


def main() -> int:
    """
    Application entry point.

    Returns:
        Application exit code.
    """

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())