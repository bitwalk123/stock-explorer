from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
)

from functions.get_info_ticker import get_info_ticker
from functions.get_standard_icon import get_standard_icon
from ui_modules.panel_ticker_info import PanelTickerInfo


class DlgInfoTicker(QDialog):
    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('企業情報 - %s.T' % code)

        name = 'SP_MessageBoxInformation'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)

        info = get_info_ticker(code)
        self.init_ui(info)
        self.resize(800, 600)

    def init_ui(self, info: dict):
        """Initialize UI
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        area = PanelTickerInfo(info)
        layout.addWidget(area)

        dlg_button = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlg_button)
        bbox.setContentsMargins(0, 0, 0, 0)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)
