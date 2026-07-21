"""
ForgeBud

Prompt Builder service.

Builds a deterministic development prompt from an
EngineeringContext.
"""

from __future__ import annotations

from models.engineering_context import EngineeringContext
from models.prompt import Prompt
from services.engineering_context_serializer import (
    EngineeringContextSerializer,
)
from services.prompt_template_service import PromptTemplateService
from services.token_estimator_service import TokenEstimatorService


class PromptBuilderService:
    """
    Builds provider-independent development prompts.
    """

    DEFAULT_TITLE = "ForgeBud Engineering Context"

    @classmethod
    def build(
        cls,
        context: EngineeringContext,
        template_key: str | None = None,
    ) -> Prompt:
        """
        Construct a Prompt from an EngineeringContext.

        Use the default prompt template when no template key is
        supplied.
        """
        markdown = EngineeringContextSerializer.to_markdown(
            context
        )

        if template_key is None:
            template = PromptTemplateService.default()
        else:
            template = PromptTemplateService.get(template_key)

        prompt_text = (
            markdown.rstrip()
            + "\n\n"
            + template.instructions.rstrip()
            + "\n\n"
            + cls._developer_instructions()
            + "\n"
        )

        return Prompt(
            title=f"{cls.DEFAULT_TITLE} — {template.name}",
            markdown=prompt_text,
            token_estimate=TokenEstimatorService.estimate(
                prompt_text
            ),
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