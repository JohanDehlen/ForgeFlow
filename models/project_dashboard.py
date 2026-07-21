"""
ForgeBud

Project dashboard model.

Represents the data displayed by the Project Dashboard.
"""

from dataclasses import dataclass, field

from models.project_context import ProjectContext
from models.project_info import ProjectInfo
from models.project_validation import ProjectValidation
from models.release_manifest import ReleaseManifest


@dataclass(slots=True)
class ProjectDashboard:
    """
    Current project state presented by the Project Dashboard.
    """

    project_info: ProjectInfo = field(
        default_factory=ProjectInfo
    )

    project_context: ProjectContext = field(
        default_factory=ProjectContext
    )

    release_manifest: ReleaseManifest = field(
        default_factory=ReleaseManifest
    )

    project_validation: ProjectValidation = field(
        default_factory=ProjectValidation
    )

    is_initialized: bool = False