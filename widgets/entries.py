from PySide6.QtWidgets import QLineEdit


class EntryTicker(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(75)
        self.setStyleSheet('QLineEdit {padding-left:5px;}')
        self.setReadOnly(True)

