from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QLabel {font-family: monospace;}')


class LabelCode(Label):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(QMargins(0, 0, 5, 0))
