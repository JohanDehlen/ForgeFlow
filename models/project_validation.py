"""
ForgeBud

Project validation model.

Represents the results of validating a ForgeBud project.
The model contains state only.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProjectValidation:
    """
    Represents the validation state of a ForgeBud project.
    """

    is_valid: bool = True

    has_forgebud_directory: bool = False

    has_project_metadata: bool = False

    missing_files: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    def add_warning(self, message: str) -> None:
        """
        Record a validation warning.
        """
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """
        Record a validation error and mark the project invalid.
        """
        self.errors.append(message)
        self.is_valid = False

    @property
    def has_warnings(self) -> bool:
        """
        Return whether validation produced warnings.
        """
        return bool(self.warnings)

    @property
    def has_errors(self) -> bool:
        """
        Return whether validation produced errors.
        """
        return bool(self.errors)