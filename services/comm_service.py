from __future__ import annotations

import random

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from services.data_model import DataModel


class CommService(QObject):
    """Simulation-first communication service.

    Emits telemetry updates every 100 ms. This interface can be replaced with
    real serial communication later without changing the UI layer.
    """

    data_updated = pyqtSignal(object)

    def __init__(self, data_model: DataModel, interval_ms: int = 100) -> None:
        super().__init__()
        self.data_model = data_model
        self.connected = False
        self._timer = QTimer(self)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(self._simulate_data)

    def start(self) -> None:
        self.connected = True
        self._timer.start()

    def stop(self) -> None:
        self.connected = False
        self._timer.stop()

    def send_command(self, command: str) -> None:
        """Stub for command transport."""
        _ = command

    def _simulate_data(self) -> None:
        self.data_model.supply_pressure1 = max(0.0, min(250.0, self.data_model.supply_pressure1 + random.uniform(-5, 5)))
        self.data_model.supply_pressure2 = max(0.0, min(250.0, self.data_model.supply_pressure2 + random.uniform(-5, 5)))
        self.data_model.return_pressure = max(0.0, min(35.0, self.data_model.return_pressure + random.uniform(-1.2, 1.2)))
        self.data_model.torque = max(-3000.0, min(3000.0, self.data_model.torque + random.uniform(-180, 180)))
        self.data_model.rpm = max(0.0, min(350.0, self.data_model.rpm + random.uniform(-15, 15)))
        self.data_model.turns = max(0.0, self.data_model.turns + random.uniform(0, 0.08))
        self.data_model.temperature = max(10.0, min(120.0, self.data_model.temperature + random.uniform(-0.8, 0.8)))
        self.data_updated.emit(self.data_model)
