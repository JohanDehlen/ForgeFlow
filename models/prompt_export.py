"""
ForgeBud

Prompt export model.

Represents the result of exporting a Prompt to an external
destination.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PromptExport:
    """
    Result of a prompt export operation.
    """

    success: bool = False

    destination: str = ""

    message: str = ""