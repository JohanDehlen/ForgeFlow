"""
ForgeBud

Prompt model.

Represents a deterministic development prompt generated from an
EngineeringContext.

The model contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Prompt:
    """
    Represents a generated development prompt.

    The PromptBuilderService is responsible for constructing
    instances of this model.
    """

    title: str = ""

    markdown: str = ""

    token_estimate: int = 0