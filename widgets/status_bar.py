"""
ForgeFlow

Application status bar.

Responsibilities:
- Display the current application status.
- Provide a simple public API for updating the status.
"""

from PySide6.QtWidgets import QLabel


class StatusBar(QLabel):
    """
    Simple application status bar.
    """

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-top: 1px solid #C0C0C0;
            }
        """)

        self.show_message("Ready")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def show_message(self, message: str) -> None:
        """
        Display a status message.

        Args:
            message: Message to display.
        """

        self.setText(message)

    def clear_message(self) -> None:
        """
        Clear the current status message.
        """

        self.show_message("")