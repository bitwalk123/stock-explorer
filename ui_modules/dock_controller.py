from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from ui_modules.dock_ticker import DockTicker


class DockController(QDockWidget):
    """Dock for controller
    """

    def __init__(self, dock_ticker: DockTicker):
        super().__init__()
        self.dock_ticker = dock_ticker
        self.setContentsMargins(0, 0, 0, 0)
        self.setTitleBarWidget(QWidget(None))
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        base = QWidget()
        self.setWidget(base)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        base.setLayout(layout)

        but = QPushButton('TEST')
        but.clicked.connect(self.on_click_button)
        but.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )
        layout.addWidget(but)

        pad = QWidget()
        pad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        layout.addWidget(pad)

    def on_click_button(self):
        print(self.dock_ticker.get_current_ticker())
