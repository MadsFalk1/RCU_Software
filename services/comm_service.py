from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from services.data_model import DataModel
from services.register_map import DIAGNOSTIC_NAMES, REGISTER_MAP
from services.register_mapping import apply_register_mapping

try:
    from pymodbus.client import ModbusSerialClient
except ImportError:  # pragma: no cover - handled at runtime in target env
    ModbusSerialClient = None


class CommService(QObject):
    """Modbus RTU communication service for Valve Pack Board / GPIO."""

    data_updated = pyqtSignal(object)
    comm_event = pyqtSignal(str)

    def __init__(
        self,
        data_model: DataModel,
        port: str = "COM3",
        slave_id: int = 1,
        baudrate: int = 38400,
        parity: str = "N",
        stopbits: int = 1,
        poll_ms: int = 200,
    ) -> None:
        super().__init__()
        self.data_model = data_model
        self.port = port
        self.slave_id = slave_id
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits

        self._client = None
        self._timer = QTimer(self)
        self._timer.setInterval(poll_ms)
        self._timer.timeout.connect(self.poll)

    def connect(self) -> bool:
        if ModbusSerialClient is None:
            self._set_error("pymodbus is not installed")
            return False

        attempts = [
            {"baudrate": self.baudrate, "parity": self.parity, "stopbits": self.stopbits, "slave_id": self.slave_id},
            {"baudrate": 115200, "parity": "N", "stopbits": 1, "slave_id": 1},
        ]

        for attempt in attempts:
            self.disconnect()
            self._client = ModbusSerialClient(
                port=self.port,
                baudrate=attempt["baudrate"],
                parity=attempt["parity"],
                stopbits=attempt["stopbits"],
                bytesize=8,
                timeout=0.3,
            )
            if self._client.connect():
                self.baudrate = int(attempt["baudrate"])
                self.parity = str(attempt["parity"])
                self.stopbits = int(attempt["stopbits"])
                self.slave_id = int(attempt["slave_id"])
                self.data_model.connected = True
                self.data_model.com_ok = False
                self.data_model.last_error = ""
                self.comm_event.emit(
                    f"Connected {self.port} @ {self.baudrate} {self.parity}{self.stopbits}, slave {self.slave_id}"
                )
                self._timer.start()
                return True

        self._set_error(f"Failed to connect on {self.port}")
        return False

    def disconnect(self) -> None:
        self._timer.stop()
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
        self.data_model.connected = False
        self.data_model.com_ok = False
        self.data_model.crc_ok = False

    def read_block(self, register: int, count: int = 1) -> list[int]:
        if self._client is None:
            raise RuntimeError("Modbus client is not connected")

        response = self._client.read_holding_registers(address=register, count=count, slave=self.slave_id)
        if response.isError():
            raise RuntimeError(str(response))
        return list(response.registers)

    def read_named(self, register_name: str) -> int | str:
        if register_name == "VERSIONSTR":
            start = REGISTER_MAP["VERSIONSTR_START"]
            count = REGISTER_MAP["VERSIONSTR_LEN"]
            words = self.read_block(start, count)
            text = "".join(chr((word >> 8) & 0xFF) + chr(word & 0xFF) for word in words).replace("\x00", "")
            return text.strip()

        address = REGISTER_MAP[register_name]
        return self.read_block(address, 1)[0]

    def poll(self) -> None:
        if self._client is None:
            return

        try:
            for name in DIAGNOSTIC_NAMES:
                value = self.read_named(name)
                self.data_model.raw_registers[name] = value
                self.data_model.diagnostics[name] = value

            self.data_model.diagnostics["VERSIONSTR"] = self.read_named("VERSIONSTR")

            for name in ["CH_SUPPLY_P1", "CH_SUPPLY_P2", "CH_RETURN_P", "CH_TORQUE", "CH_RPM", "CH_TURNS", "CH_TEMP"]:
                self.data_model.raw_registers[name] = self.read_named(name)

            apply_register_mapping(self.data_model)
            self._update_health()
            self.data_model.last_update = datetime.now()
            self.data_updated.emit(self.data_model)
        except Exception as exc:
            self.data_model.com_ok = False
            self.data_model.crc_ok = False
            self._set_error(str(exc))
            self.data_updated.emit(self.data_model)

    def _update_health(self) -> None:
        current_count = int(self.data_model.raw_registers.get("COUNT", -1))
        previous = self.data_model.last_count
        self.data_model.com_ok = previous is None or current_count != previous
        self.data_model.crc_ok = True
        self.data_model.last_count = current_count

        err_code = int(self.data_model.raw_registers.get("ERR", 0))
        if err_code:
            self.data_model.last_error = f"Device ERR={err_code}"
            self.comm_event.emit(self.data_model.last_error)

    def _set_error(self, message: str) -> None:
        self.data_model.last_error = message
        self.comm_event.emit(message)
