from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SettingsStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (Path(__file__).resolve().parent.parent / "settings.json")

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

        return data if isinstance(data, dict) else {}

    def save(self, settings: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(settings, indent=2, sort_keys=True), encoding="utf-8")
