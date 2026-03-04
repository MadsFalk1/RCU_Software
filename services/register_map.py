from __future__ import annotations

# NOTE: Addresses below are intentionally centralized and easy to adjust to the
# exact Tech Sheet Rev G register map used in your deployment.
REGISTER_MAP: dict[str, int] = {
    "COUNT": 0x0000,
    "ERR": 0x0001,
    "MODBUSADDR": 0x0002,
    "BAUD0": 0x0003,
    "DPS0": 0x0004,
    "BVER": 0x0005,
    "FVER": 0x0006,
    "VERSIONSTR_START": 0x0010,
    "VERSIONSTR_LEN": 8,  # number of 16-bit registers to decode as ASCII
    # Placeholder process channels for easy remapping once confirmed:
    "CH_SUPPLY_P1": 0x0100,
    "CH_SUPPLY_P2": 0x0101,
    "CH_RETURN_P": 0x0102,
    "CH_TORQUE": 0x0103,
    "CH_RPM": 0x0104,
    "CH_TURNS": 0x0105,
    "CH_TEMP": 0x0106,
}

DIAGNOSTIC_NAMES = ["COUNT", "ERR", "MODBUSADDR", "BAUD0", "DPS0", "BVER", "FVER"]
