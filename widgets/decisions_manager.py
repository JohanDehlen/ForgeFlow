"""
ForgeBud

Decisions manager widget.

Displays and edits engineering decisions for an initialized ForgeBud
project. The widget contains presentation logic only and does not
access project files or services.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from models.decisions import Decisions


class DecisionsManagerWidget(QWidget):
    """
    Displays editable decisions Markdown and emits save requests.
    """

    saveRequested = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self._create_ui()
        self._connect_signals()
        self.clear()
        self.disable_editing()

    def _create_ui(self) -> None:
        """
        Create and arrange the decisions controls.
        """
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Engineering Decisions")
        main_layout.addWidget(title_label)

        self.decisionsEditor = QTextEdit()
        self.decisionsEditor.setAcceptRichText(False)
        self.decisionsEditor.setPlaceholderText(
            "Open an initialized ForgeBud project to manage "
            "its engineering decisions."
        )
        main_layout.addWidget(self.decisionsEditor)

        self.saveButton = QPushButton("Save Decisions")
        main_layout.addWidget(self.saveButton)

    def _connect_signals(self) -> None:
        """
        Connect internal controls to widget signals.
        """
        self.saveButton.clicked.connect(
            self._request_save
        )

    def set_decisions(
        self,
        decisions: Decisions,
    ) -> None:
        """
        Display the supplied decisions state.
        """
        self.decisionsEditor.setPlainText(
            decisions.markdown
        )

    def current_markdown(self) -> str:
        """
        Return the Markdown currently displayed by the editor.
        """
        return self.decisionsEditor.toPlainText()

    def clear(self) -> None:
        """
        Clear the displayed decisions document.
        """
        self.decisionsEditor.clear()

    def enable_editing(self) -> None:
        """
        Enable decisions editing and saving.
        """
        self.decisionsEditor.setEnabled(True)
        self.saveButton.setEnabled(True)

    def disable_editing(self) -> None:
        """
        Disable decisions editing and saving.
        """
        self.decisionsEditor.setEnabled(False)
        self.saveButton.setEnabled(False)

    def _request_save(self) -> None:
        """
        Emit the current editor contents as a save request.
        """
        self.saveRequested.emit(
            self.current_markdown()
        )