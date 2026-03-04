from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from services.data_model import DataModel
from widgets.gauge_widget import AnalogGaugeWidget
from widgets.status_indicator import LedIndicator


class OperationPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.gauge_supply1 = AnalogGaugeWidget("Supply Pressure 1 [bar] (HF1 & LF2)", 0, 250, "bar")
        self.gauge_supply2 = AnalogGaugeWidget("Supply Pressure 2 [bar]", 0, 250, "bar")
        self.gauge_return = AnalogGaugeWidget("Return Pressure", 0, 35, "bar")
        self.gauge_torque = AnalogGaugeWidget("Torque", -3000, 3000, "Nm")

        self.rpm_field = QLineEdit("0.0")
        self.turns_field = QLineEdit("0.0")
        self.temp_field = QLineEdit("0.0")

        self.ind_water = LedIndicator("Water Alarm")
        self.ind_com = LedIndicator("Com OK")
        self.ind_crc = LedIndicator("CRC OK")

        self._build_ui()

    def _build_ui(self) -> None:
        main = QVBoxLayout(self)

        gauges = QGridLayout()
        gauges.addWidget(self.gauge_supply1, 0, 0)
        gauges.addWidget(self.gauge_supply2, 0, 1)
        gauges.addWidget(self.gauge_return, 0, 2)
        gauges.addWidget(self.gauge_torque, 0, 3)

        info_box = QGroupBox("Torque Details")
        info_form = QFormLayout(info_box)
        info_form.addRow("RPM", self.rpm_field)
        info_form.addRow("Turns", self.turns_field)
        gauges.addWidget(info_box, 1, 3)

        main.addLayout(gauges)

        controls = QGridLayout()
        labels = ["FCR/WH CL", "FCST/...", "TRT CL/CL", "Turn Limit"]
        for i, title in enumerate(labels):
            controls.addWidget(self._soft_start_block(title), 0, i)

        turn_limit = QGroupBox("Turn Limit")
        turn_form = QFormLayout(turn_limit)
        turn_form.addRow("Turn Limit Enable", QCheckBox())
        turn_form.addRow("Limit Value", QLineEdit("2500"))
        turn_form.addRow("Turn Limitation ON", LedIndicator(""))

        torque_control = QGroupBox("Torque Control")
        torque_layout = QVBoxLayout(torque_control)
        mode = QComboBox()
        mode.addItems(["Auto", "Manual", "Soft Start"])
        torque_layout.addWidget(mode)
        torque_layout.addWidget(QPushButton("Zero Adjust"))
        torque_layout.addWidget(QPushButton("Reset Turn"))

        right_controls = QGroupBox("Panel Controls")
        rc_layout = QVBoxLayout(right_controls)
        rc_layout.addWidget(QPushButton("Remote Panel On/Off"))
        rc_layout.addWidget(QPushButton("Start Com"))
        rc_layout.addWidget(self.ind_water)
        rc_layout.addWidget(self.ind_com)
        rc_layout.addWidget(self.ind_crc)
        rc_layout.addWidget(QLabel("Temp"))
        rc_layout.addWidget(self.temp_field)

        controls.addWidget(turn_limit, 1, 0, 1, 2)
        controls.addWidget(torque_control, 1, 2)
        controls.addWidget(right_controls, 1, 3)

        main.addLayout(controls)

    def _soft_start_block(self, title: str) -> QGroupBox:
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        layout.addWidget(slider)
        layout.addWidget(QLineEdit("0"))
        layout.addWidget(QPushButton("Latch"))
        return box

    def update_data(self, data: DataModel) -> None:
        self.gauge_supply1.set_value(data.supply_pressure1)
        self.gauge_supply2.set_value(data.supply_pressure2)
        self.gauge_return.set_value(data.return_pressure)
        self.gauge_torque.set_value(data.torque)
        self.rpm_field.setText(f"{data.rpm:.1f}")
        self.turns_field.setText(f"{data.turns:.2f}")
        self.temp_field.setText(f"{data.temperature:.1f}")
        self.ind_com.set_on(True)
        self.ind_crc.set_on(True)
        self.ind_water.set_on(data.temperature > 90)
