"""
ForgeBud

File service.

Responsibilities:
- Read files.
- Write files.
- Create folders.
- Enumerate project files.
- Never contain Git or AI logic.
"""

from __future__ import annotations

from pathlib import Path


class FileService:
    """
    Service responsible for filesystem operations.
    """

    @staticmethod
    def exists(path: str | Path) -> bool:
        """
        Return True if the path exists.
        """

        return Path(path).exists()

    @staticmethod
    def read_text(path: str | Path) -> str:
        """
        Read a UTF-8 text file.

        Returns an empty string if the file cannot be read.
        """

        try:
            return Path(path).read_text(
                encoding="utf-8"
            )

        except Exception:
            return ""

    @staticmethod
    def write_text(
        path: str | Path,
        text: str,
    ) -> None:
        """
        Write UTF-8 text to a file.
        Parent folders are created automatically.
        """

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            text,
            encoding="utf-8",
        )

    @staticmethod
    def create_directory(path: str | Path) -> None:
        """
        Create a directory if it does not exist.
        """

        Path(path).mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def list_files(
        folder: str | Path,
        pattern: str = "*",
    ) -> list[Path]:
        """
        Return files matching a glob pattern.
        """

        folder = Path(folder)

        if not folder.exists():
            return []

        return sorted(
            file
            for file in folder.rglob(pattern)
            if file.is_file()
        )

    @staticmethod
    def relative_path(
        file: str | Path,
        root: str | Path,
    ) -> str:
        """
        Return a path relative to the project root.
        """

        return str(
            Path(file).relative_to(Path(root))
        )

    @staticmethod
    def file_size(
        path: str | Path,
    ) -> int:
        """
        Return the file size in bytes.
        """

        try:
            return Path(path).stat().st_size

        except Exception:
            return 0