"""
ForgeBud

Clipboard export service.

Exports a Prompt to the system clipboard.
"""

from __future__ import annotations

from PySide6.QtGui import QGuiApplication

from models.prompt import Prompt
from models.prompt_export import PromptExport


class ClipboardExportService:
    """
    Exports prompts to the system clipboard.
    """

    DESTINATION = "Clipboard"

    @classmethod
    def export(
        cls,
        prompt: Prompt,
    ) -> PromptExport:
        """
        Copy the supplied Prompt to the system clipboard.
        """
        clipboard = QGuiApplication.clipboard()

        clipboard.setText(prompt.markdown)

        return PromptExport(
            success=True,
            destination=cls.DESTINATION,
            message="Prompt copied to clipboard.",
        )