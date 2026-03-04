from __future__ import annotations

import pyqtgraph as pg
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from services.data_model import DataModel


class GraphPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.x_data: list[float] = []
        self.y_data: list[float] = []
        self.time_s = 0.0

        layout = QHBoxLayout(self)
        self.plot = pg.PlotWidget()
        self.plot.setLabel("left", "Torque [Nm]")
        self.plot.setLabel("bottom", "Time", units="s")
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.plot.plot(pen=pg.mkPen("#f5922b", width=2))
        layout.addWidget(self.plot, stretch=4)

        side = QVBoxLayout()
        self.btn_start = QPushButton("Start Plot")
        self.btn_time = QPushButton("X-axis Time")
        self.btn_report = QPushButton("Generate Report")
        self.btn_clear = QPushButton("Clear Graph")
        self.btn_clear.clicked.connect(self.clear)
        for btn in [self.btn_start, self.btn_time, self.btn_report, self.btn_clear]:
            side.addWidget(btn)
        side.addStretch(1)
        layout.addLayout(side, stretch=1)

    def add_point(self, data: DataModel) -> None:
        self.time_s += 0.1
        self.x_data.append(self.time_s)
        self.y_data.append(data.torque)
        if len(self.x_data) > 500:
            self.x_data = self.x_data[-500:]
            self.y_data = self.y_data[-500:]
        self.curve.setData(self.x_data, self.y_data)

    def clear(self) -> None:
        self.x_data.clear()
        self.y_data.clear()
        self.time_s = 0.0
        self.curve.clear()
