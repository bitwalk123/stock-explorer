from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QLabel, QLCDNumber


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QLabel {font-family: monospace;}')


class LabelCode(Label):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(QMargins(0, 0, 5, 0))


class LCDNumber(QLCDNumber):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedWidth(150)
        self.setFixedHeight(24)
        self.setDigitCount(10)
        self.display('0.0')
