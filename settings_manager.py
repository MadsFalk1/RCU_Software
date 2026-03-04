"""Shared settings storage for GUI and scripts.

All scripts should call `load_settings()` to read the current values from
`settings.json`. The GUI should call `save_settings()` after updates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "light",
    "refresh_interval": 30,
    "auto_start": False,
    "output_directory": "./output",
}


def ensure_settings_file() -> Path:
    """Create settings.json with defaults if it does not exist."""
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
    return SETTINGS_PATH


def load_settings() -> Dict[str, Any]:
    """Load settings from disk and merge in missing defaults."""
    ensure_settings_file()

    with SETTINGS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    merged = {**DEFAULT_SETTINGS, **data}
    # Keep file up-to-date if defaults were newly introduced.
    if merged != data:
        save_settings(merged)

    return merged


def save_settings(settings: Dict[str, Any]) -> None:
    """Persist settings atomically to JSON."""
    merged = {**DEFAULT_SETTINGS, **settings}
    tmp_file = SETTINGS_PATH.with_suffix(".json.tmp")

    with tmp_file.open("w", encoding="utf-8") as file:
        json.dump(merged, file, indent=2)
        file.write("\n")

    tmp_file.replace(SETTINGS_PATH)
