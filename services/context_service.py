"""
ForgeBud

Context service.

Responsibilities:
- Build the current ProjectContext.
- Coordinate information from other services.
- Provide a single source of project information.
"""

from pathlib import Path

from models.project_context import ProjectContext
from services.git_service import GitService


class ContextService:
    """
    Builds ProjectContext objects from the current project.
    """

    @staticmethod
    def build(project_path: str) -> ProjectContext:
        """
        Build a ProjectContext for the specified project.

        Args:
            project_path: Path to the project folder.

        Returns:
            A populated ProjectContext instance.
        """

        context = ProjectContext()

        context.project_path = project_path

        if not project_path:
            return context

        project = Path(project_path)

        if not project.exists():
            return context

        context.is_repository = GitService.is_repository(project)

        if not context.is_repository:
            return context

        context.branch = GitService.current_branch(project)

        context.last_commit = GitService.last_commit(project)

        context.changed_files = GitService.changed_files(project)

        context.untracked_files = GitService.untracked_files(project)

        context.status = GitService.status(project)

        return context