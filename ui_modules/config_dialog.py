from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QTabWidget, QVBoxLayout, QDialogButtonBox,
)

from functions.resources import get_standard_icon
from ui_modules.panel_db import PanelDB


class DlgConfig(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('設定')
        name = 'SP_FileDialogDetailedView'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        tab = QTabWidget()
        layout.addWidget(tab)

        panel_db = PanelDB()
        tab.addTab(panel_db, panel_db.getTabLabel())

        dlg_button = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlg_button)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)
