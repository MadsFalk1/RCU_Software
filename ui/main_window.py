from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QTabWidget, QVBoxLayout, QWidget

from services.comm_service import CommService
from services.data_model import DataModel
from ui.aux_page import AuxPage
from ui.graph_page import GraphPage
from ui.log_setup_page import LogSetupPage
from ui.operation_page import OperationPage
from ui.setup_page import SetupPage


class MainWindow(QMainWindow):
    def __init__(self, model: DataModel, comm_service: CommService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model = model
        self.comm_service = comm_service

        self.setWindowTitle("RCU OAS Control Panel")
        self.resize(1600, 950)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        header = QHBoxLayout()
        logo = QLabel("OCEANEERING")
        logo.setObjectName("logoLabel")
        version = QLabel("RCU OAS 2.1.4")
        version.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        version.setObjectName("versionLabel")
        header.addWidget(logo)
        header.addStretch(1)
        header.addWidget(version)

        layout.addLayout(header)

        self.tabs = QTabWidget()
        self.operation_page = OperationPage()
        self.log_setup_page = LogSetupPage()
        self.graph_page = GraphPage()
        self.aux_page = AuxPage()
        self.setup_page = SetupPage()

        self.tabs.addTab(self.operation_page, "Operation Page")
        self.tabs.addTab(self.log_setup_page, "Log Setup")
        self.tabs.addTab(self.graph_page, "Graph")
        self.tabs.addTab(self.aux_page, "Aux")
        self.tabs.addTab(self.setup_page, "Setup")
        layout.addWidget(self.tabs)

        self.comm_service.data_updated.connect(self._on_data_update)

    def _on_data_update(self, data: DataModel) -> None:
        self.operation_page.update_data(data)
        self.graph_page.add_point(data)
