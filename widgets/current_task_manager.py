"""
ForgeBud

Current task manager widget.

Displays and edits the current task for an initialized ForgeBud
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

from models.current_task import CurrentTask


class CurrentTaskManagerWidget(QWidget):
    """
    Displays editable current-task Markdown and emits save requests.
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
        Create and arrange the current-task controls.
        """
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Current Task")
        main_layout.addWidget(title_label)

        self.taskEditor = QTextEdit()
        self.taskEditor.setAcceptRichText(False)
        self.taskEditor.setPlaceholderText(
            "Open an initialized ForgeBud project to manage "
            "its current task."
        )
        main_layout.addWidget(self.taskEditor)

        self.saveButton = QPushButton("Save Current Task")
        main_layout.addWidget(self.saveButton)

    def _connect_signals(self) -> None:
        """
        Connect internal controls to widget signals.
        """
        self.saveButton.clicked.connect(
            self._request_save
        )

    def set_current_task(
        self,
        current_task: CurrentTask,
    ) -> None:
        """
        Display the supplied current-task state.
        """
        self.taskEditor.setPlainText(
            current_task.markdown
        )

    def current_markdown(self) -> str:
        """
        Return the Markdown currently displayed by the editor.
        """
        return self.taskEditor.toPlainText()

    def clear(self) -> None:
        """
        Clear the displayed current-task document.
        """
        self.taskEditor.clear()

    def enable_editing(self) -> None:
        """
        Enable current-task editing and saving.
        """
        self.taskEditor.setEnabled(True)
        self.saveButton.setEnabled(True)

    def disable_editing(self) -> None:
        """
        Disable current-task editing and saving.
        """
        self.taskEditor.setEnabled(False)
        self.saveButton.setEnabled(False)

    def _request_save(self) -> None:
        """
        Emit the current editor contents as a save request.
        """
        self.saveRequested.emit(
            self.current_markdown()
        )