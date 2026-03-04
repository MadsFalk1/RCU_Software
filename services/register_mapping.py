from __future__ import annotations

from services.data_model import DataModel


def apply_register_mapping(model: DataModel) -> None:
    """Translate raw Modbus values into engineering placeholders for UI.

    Keep all channel mapping logic centralized here so real signal binding can be
    updated in one place once register/channel confirmations are complete.
    """

    raw = model.raw_registers
    derived = model.derived_values

    derived["supply_pressure1"] = float(raw.get("CH_SUPPLY_P1", 0.0))
    derived["supply_pressure2"] = float(raw.get("CH_SUPPLY_P2", 0.0))
    derived["return_pressure"] = float(raw.get("CH_RETURN_P", 0.0))
    derived["torque"] = _to_signed(raw.get("CH_TORQUE", 0))
    derived["rpm"] = float(raw.get("CH_RPM", 0.0))
    derived["turns"] = float(raw.get("CH_TURNS", 0.0))
    derived["temperature"] = float(raw.get("CH_TEMP", 0.0))


def _to_signed(value: int | float) -> float:
    if not isinstance(value, int):
        return float(value)
    if value > 0x7FFF:
        return float(value - 0x10000)
    return float(value)
