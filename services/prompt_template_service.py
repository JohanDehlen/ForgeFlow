"""
ForgeBud

Prompt template service.

Provides the built-in provider-independent prompt templates used by
the Prompt Builder.
"""

from __future__ import annotations

from models.prompt_template import PromptTemplate


class PromptTemplateService:
    """
    Provides ForgeBud's built-in prompt templates.
    """

    DEFAULT_TEMPLATE_KEY = "coding"

    _TEMPLATES = (
        PromptTemplate(
            key="coding",
            name="Coding",
            instructions="""# Task Instructions

Implement the current development task.

- Follow the current release objective.
- Preserve the existing architecture.
- Follow the project's coding standards.
- Make only changes required for the task.
- Return complete replacement files when code changes are needed.
- Do not include placeholders or incomplete implementations.
""",
        ),
        PromptTemplate(
            key="bug_fix",
            name="Bug Fix",
            instructions="""# Task Instructions

Investigate and fix the reported problem.

- Identify the root cause before changing code.
- Preserve unrelated existing behavior.
- Make the smallest complete correction.
- Consider failure paths and edge cases.
- Return complete replacement files when code changes are needed.
- Include clear validation steps.
""",
        ),
        PromptTemplate(
            key="refactor",
            name="Refactor",
            instructions="""# Task Instructions

Refactor the requested area without changing intended behavior.

- Preserve public interfaces unless explicitly instructed otherwise.
- Reduce duplication and improve responsibility boundaries.
- Keep the implementation simple and readable.
- Avoid unrelated changes.
- Return complete replacement files when code changes are needed.
- Explain any meaningful architectural trade-offs.
""",
        ),
        PromptTemplate(
            key="documentation",
            name="Documentation",
            instructions="""# Task Instructions

Create or update the requested documentation.

- Keep documentation consistent with the current implementation.
- Use clear headings and concise language.
- Explain important behavior, constraints, and decisions.
- Do not describe features that do not exist.
- Return complete replacement documents.
""",
        ),
        PromptTemplate(
            key="architecture_review",
            name="Architecture Review",
            instructions="""# Task Instructions

Review the project architecture using the Engineering Context.

- Identify responsibility violations and unnecessary coupling.
- Check consistency with the documented architecture.
- Highlight risks, missing abstractions, and over-engineering.
- Prioritize issues that affect the current release.
- Do not propose speculative features unrelated to the task.
- Provide practical, ordered recommendations.
""",
        ),
    )

    @classmethod
    def all(cls) -> tuple[PromptTemplate, ...]:
        """
        Return all built-in prompt templates.
        """
        return cls._TEMPLATES

    @classmethod
    def get(cls, key: str) -> PromptTemplate:
        """
        Return the template matching the supplied key.

        Raise ValueError when the key is unknown.
        """
        normalized_key = key.strip().lower()

        for template in cls._TEMPLATES:
            if template.key == normalized_key:
                return template

        raise ValueError(
            f"Unknown prompt template: {key}"
        )

    @classmethod
    def default(cls) -> PromptTemplate:
        """
        Return the default prompt template.
        """
        return cls.get(cls.DEFAULT_TEMPLATE_KEY)