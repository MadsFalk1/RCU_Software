from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SetupPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        data_rw = QGroupBox("Data Read / Write")
        rw_form = QFormLayout(data_rw)
        rw_form.addRow("Data Read", QTextEdit())
        rw_form.addRow("Data Write", QTextEdit())

        cal = QGroupBox("Analog Calibration")
        cal_grid = QGridLayout(cal)
        labels = [
            "Select Channel",
            "AD In",
            "Calculated Value",
            "ADC Value 1",
            "ADC Value 2",
            "Sensor Value 1",
            "Sensor Value 2",
            "Zero Value",
            "Node No",
            "Channel No",
        ]
        for i, name in enumerate(labels):
            cal_grid.addWidget(QLabel(name), i, 0)
            cal_grid.addWidget(QLineEdit(), i, 1)
        cal_grid.addWidget(QPushButton("To ADC Value 1"), len(labels), 0)
        cal_grid.addWidget(QPushButton("To ADC Value 2"), len(labels), 1)
        cal_grid.addWidget(QPushButton("Calculated Value → Zero Value"), len(labels) + 1, 0, 1, 2)

        misc = QGroupBox("Misc Settings Subsea")
        misc_form = QFormLayout(misc)
        for name in ["fq1", "fq2", "Gain1", "Gain2", "Address"]:
            misc_form.addRow(name, QLineEdit())
        misc_form.addRow("", QPushButton("Write Subsea Default"))

        remote = QGroupBox("Remote Panel")
        remote_form = QFormLayout(remote)
        remote_form.addRow("Start Com Remote Panel", QPushButton("Start"))
        remote_form.addRow("Com Port", QLineEdit("COM1"))
        remote_form.addRow("Data Read Remote Panel", QTextEdit())
        remote_form.addRow("", QCheckBox("Reset all functions when Remote Panel is disabled"))

        comm = QGroupBox("Topside Comm Settings")
        comm_form = QFormLayout(comm)
        self.com_port = QLineEdit("COM3")
        self.slave_id = QLineEdit("1")
        self.baud_rate = QLineEdit("38400")
        self.parity = QLineEdit("N")
        self.stop_bits = QLineEdit("1")
        self.btn_connect = QPushButton("Connect COM3")
        self.btn_disconnect = QPushButton("Disconnect")
        comm_form.addRow("Device", QLineEdit("Moxa Uport 1150"))
        comm_form.addRow("Comm Type", QLineEdit("RS232 Modbus RTU"))
        comm_form.addRow("Com Port", self.com_port)
        comm_form.addRow("Slave ID", self.slave_id)
        comm_form.addRow("Baud Rate", self.baud_rate)
        comm_form.addRow("Parity (N/E/O)", self.parity)
        comm_form.addRow("Stop Bits", self.stop_bits)

        button_row = QHBoxLayout()
        button_row.addWidget(self.btn_connect)
        button_row.addWidget(self.btn_disconnect)
        comm_form.addRow(button_row)

        diagnostics = QGroupBox("Diagnostics")
        diag_layout = QVBoxLayout(diagnostics)
        self.diag_text = QTextEdit()
        self.diag_text.setReadOnly(True)
        self.comm_log = QTextEdit()
        self.comm_log.setReadOnly(True)
        diag_layout.addWidget(QLabel("Device Registers"))
        diag_layout.addWidget(self.diag_text)
        diag_layout.addWidget(QLabel("Comm Log"))
        diag_layout.addWidget(self.comm_log)

        layout.addWidget(data_rw)
        layout.addWidget(cal)
        layout.addWidget(misc)
        row2 = QHBoxLayout()
        row2.addWidget(remote)
        row2.addWidget(comm)
        layout.addLayout(row2)
        layout.addWidget(diagnostics)

    def comm_params(self) -> dict[str, Any]:
        return {
            "port": self.com_port.text().strip() or "COM3",
            "slave_id": int(self.slave_id.text().strip() or 1),
            "baudrate": int(self.baud_rate.text().strip() or 38400),
            "parity": (self.parity.text().strip() or "N").upper(),
            "stopbits": int(self.stop_bits.text().strip() or 1),
        }

    def set_diagnostics(self, values: dict[str, Any]) -> None:
        lines = [f"{k}: {v}" for k, v in values.items()]
        self.diag_text.setPlainText("\n".join(lines))

    def append_log(self, line: str) -> None:
        if not line:
            return
        self.comm_log.append(line)
