from PySide6.QtWidgets import QMessageBox

from funcs.common import get_standard_icon


class DialogAlert(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        name = 'SP_FileDialogInfoView'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)

        self.setWindowTitle('Warning')
        self.setStandardButtons(
            QMessageBox.StandardButton.Ok
        )
        self.setIcon(QMessageBox.Icon.Critical)
