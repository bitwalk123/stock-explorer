from PySide6.QtWidgets import QMessageBox


class DialogWarning(QMessageBox):
    def __init__(self, msg:str):
        super().__init__()
        self.setWindowTitle('警告')
        self.setText(msg)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Warning)
