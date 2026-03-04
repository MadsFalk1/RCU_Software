from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DataModel:
    """Holds runtime values used across UI pages."""

    supply_pressure1: float = 0.0
    supply_pressure2: float = 0.0
    return_pressure: float = 0.0
    torque: float = 0.0
    rpm: float = 0.0
    turns: float = 0.0
    temperature: float = 0.0
