from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from functions.get_volume_median_with_code_start import get_volume_median_with_code_start
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain


class DockController(QDockWidget):
    """Dock for controller
    """

    def __init__(self, toolbar: ToolBarMain, dock_ticker: DockTicker):
        super().__init__()
        self.toolbar = toolbar
        self.dock_ticker = dock_ticker
        self.setTitleBarWidget(QWidget(None))
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        base = QWidget()
        self.setWidget(base)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 5)
        base.setLayout(layout)

        but = QPushButton('TEST')
        but.clicked.connect(self.on_click_button)
        but.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )
        layout.addWidget(but)

        # padding horizontally
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        layout.addWidget(hpad)

    def on_click_button(self):
        """Handle buttonclick event
        """
        code: int = self.dock_ticker.get_current_ticker()
        start = self.toolbar.get_start_date()
        volume_median = get_volume_median_with_code_start(code, start)
        print('code:', code, ', volume(median):', volume_median)
