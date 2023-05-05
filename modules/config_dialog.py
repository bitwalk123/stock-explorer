from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)

from functions.get_standard_ison import get_standard_icon
from modules.panel_db import PanelDB


class DlgConfig(QMainWindow):
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
        tab = QTabWidget()
        self.setCentralWidget(tab)

        panel_db = PanelDB()
        tab.addTab(panel_db, panel_db.getTabLabel())


