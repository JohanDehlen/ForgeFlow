"""
ForgeBud

Git service.

Responsibilities:
- Detect whether a folder is a Git repository.
- Read Git information.
- Never modify the repository.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitService:
    """
    Read-only interface to Git.
    """

    @staticmethod
    def _run(repo: str | Path, *args: str) -> str:
        """
        Execute a git command and return its output.

        Returns an empty string if the command fails.
        """

        repo = Path(repo)

        try:
            result = subprocess.run(
                ["git", *args],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip()

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
        ):
            return ""

    # -------------------------------------------------
    # Repository
    # -------------------------------------------------

    @classmethod
    def is_repository(cls, repo: str | Path) -> bool:
        """
        Determine whether the folder is a Git repository.
        """

        return (
            cls._run(repo, "rev-parse", "--is-inside-work-tree")
            == "true"
        )

    # -------------------------------------------------
    # Branch
    # -------------------------------------------------

    @classmethod
    def current_branch(cls, repo: str | Path) -> str:
        """
        Return the current branch name.
        """

        return cls._run(
            repo,
            "branch",
            "--show-current",
        )

    # -------------------------------------------------
    # Last Commit
    # -------------------------------------------------

    @classmethod
    def last_commit(cls, repo: str | Path) -> str:
        """
        Return the last commit summary.
        """

        return cls._run(
            repo,
            "log",
            "-1",
            "--pretty=%s",
        )

    # -------------------------------------------------
    # Modified Files
    # -------------------------------------------------

    @classmethod
    def changed_files(cls, repo: str | Path) -> list[str]:
        """
        Return modified tracked files.
        """

        output = cls._run(
            repo,
            "diff",
            "--name-only",
        )

        if not output:
            return []

        return output.splitlines()

    # -------------------------------------------------
    # Untracked Files
    # -------------------------------------------------

    @classmethod
    def untracked_files(cls, repo: str | Path) -> list[str]:
        """
        Return untracked files.
        """

        output = cls._run(
            repo,
            "ls-files",
            "--others",
            "--exclude-standard",
        )

        if not output:
            return []

        return output.splitlines()

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    @classmethod
    def status(cls, repo: str | Path) -> str:
        """
        Return the short Git status.
        """

        return cls._run(
            repo,
            "status",
            "--short",
        )