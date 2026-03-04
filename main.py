from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from services.comm_service import CommService
from services.data_model import DataModel
from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "styles" / "dark_theme.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text())


def main() -> int:
    app = QApplication(sys.argv)
    load_stylesheet(app)

    model = DataModel()
    comm_service = CommService(model)
    window = MainWindow(model, comm_service)
    window.show()

    comm_service.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
