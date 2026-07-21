"""
ForgeBud

Prompt Builder service.

Builds a deterministic development prompt from an EngineeringContext.
"""

from __future__ import annotations

from models.engineering_context import EngineeringContext
from models.prompt import Prompt
from services.engineering_context_serializer import (
    EngineeringContextSerializer,
)


class PromptBuilderService:
    """
    Builds provider-independent development prompts.
    """

    DEFAULT_TITLE = (
        "ForgeBud Engineering Context"
    )

    @classmethod
    def build(
        cls,
        context: EngineeringContext,
    ) -> Prompt:
        """
        Construct a Prompt from an EngineeringContext.
        """
        markdown = EngineeringContextSerializer.to_markdown(
            context
        )

        instructions = cls._developer_instructions()

        prompt_text = (
            markdown.rstrip()
            + "\n\n"
            + instructions
            + "\n"
        )

        return Prompt(
            title=cls.DEFAULT_TITLE,
            markdown=prompt_text,
            token_estimate=0,
        )

    @staticmethod
    def _developer_instructions() -> str:
        """
        Return the standard ForgeBud developer instructions.
        """
        return """# Developer Instructions

Use the Engineering Context above as the source of truth.

Before generating code:

- Read and understand the complete context.
- Preserve the existing architecture.
- Follow the project's coding standards.
- Do not invent missing project state.
- Replace complete files rather than partial fragments unless explicitly requested.
- Keep changes consistent with the current release objective.
- Explain architectural concerns before implementation if they materially affect the design.
"""