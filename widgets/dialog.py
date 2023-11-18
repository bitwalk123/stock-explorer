from PySide6.QtWidgets import QMessageBox

from functions.get_standard_icon import get_standard_icon


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


class DialogConfirmationYesCancel(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        name = 'SP_MessageBoxWarning'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)

        self.setWindowTitle('Confirmation')
        self.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        self.setDefaultButton(QMessageBox.StandardButton.Cancel)
        self.setIcon(QMessageBox.Icon.Warning)
