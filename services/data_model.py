from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DataModel:
    """Shared runtime model for comm state, raw register values and derived UI values."""

    raw_registers: dict[str, Any] = field(default_factory=dict)
    derived_values: dict[str, float] = field(default_factory=lambda: {
        "supply_pressure1": 0.0,
        "supply_pressure2": 0.0,
        "return_pressure": 0.0,
        "torque": 0.0,
        "rpm": 0.0,
        "turns": 0.0,
        "temperature": 0.0,
    })

    connected: bool = False
    com_ok: bool = False
    crc_ok: bool = False
    last_error: str = ""
    last_count: int | None = None
    last_update: datetime | None = None

    diagnostics: dict[str, Any] = field(default_factory=dict)
