"""
ForgeBud

Application settings service.

Responsibilities:
- Load application settings.
- Save application settings.
- Ensure the configuration directory exists.
"""

from __future__ import annotations

import json
from pathlib import Path


class SettingsService:
    """
    Service responsible for loading and saving
    ForgeBud application settings.
    """

    CONFIG_DIR = Path("config")
    SETTINGS_FILE = CONFIG_DIR / "settings.json"

    DEFAULT_SETTINGS = {
        "last_project": "",
        "window_width": 1400,
        "window_height": 900,
        "window_x": None,
        "window_y": None,
    }

    @classmethod
    def load(cls) -> dict:
        """
        Load application settings.

        Returns:
            Dictionary containing the application settings.
        """

        cls._ensure_config_exists()

        if not cls.SETTINGS_FILE.exists():
            cls.save(cls.DEFAULT_SETTINGS)
            return cls.DEFAULT_SETTINGS.copy()

        try:
            with open(cls.SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)

        except Exception:
            settings = cls.DEFAULT_SETTINGS.copy()

        # Ensure any newly added settings exist
        for key, value in cls.DEFAULT_SETTINGS.items():
            settings.setdefault(key, value)

        return settings

    @classmethod
    def save(cls, settings: dict) -> None:
        """
        Save application settings.
        """

        cls._ensure_config_exists()

        with open(cls.SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                settings,
                file,
                indent=4,
                ensure_ascii=False,
            )

    @classmethod
    def get(cls, key: str, default=None):
        """
        Retrieve a single setting.
        """

        settings = cls.load()

        return settings.get(key, default)

    @classmethod
    def set(cls, key: str, value) -> None:
        """
        Store a single setting.
        """

        settings = cls.load()

        settings[key] = value

        cls.save(settings)

    @classmethod
    def _ensure_config_exists(cls) -> None:
        """
        Ensure the configuration directory exists.
        """

        cls.CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )