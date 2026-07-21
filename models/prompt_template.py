"""
ForgeBud

Prompt template model.

Represents a provider-independent set of instructions applied when
building an engineering prompt.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PromptTemplate:
    """
    Defines one selectable prompt-building template.
    """

    key: str

    name: str

    instructions: str