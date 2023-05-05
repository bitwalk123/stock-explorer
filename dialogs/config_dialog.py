from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from functions.get_standard_ison import get_standard_icon


class DlgConfig(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle('設定')
        name = 'SP_FileDialogDetailedView'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)

