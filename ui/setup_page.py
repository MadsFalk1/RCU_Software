from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget


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
            "Select Channel", "AD In", "Calculated Value", "ADC Value 1", "ADC Value 2",
            "Sensor Value 1", "Sensor Value 2", "Zero Value", "Node No", "Channel No",
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
        comm_form.addRow("Device", QLineEdit("Moxa Uport 1150"))
        comm_form.addRow("Comm Type", QLineEdit("RS232"))
        comm_form.addRow("Baud Rate", QLineEdit("38400"))
        comm_form.addRow("Data layer", QLineEdit("8N1"))

        layout.addWidget(data_rw)
        layout.addWidget(cal)
        layout.addWidget(misc)
        row2 = QHBoxLayout()
        row2.addWidget(remote)
        row2.addWidget(comm)
        layout.addLayout(row2)
