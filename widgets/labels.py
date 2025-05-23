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
        self.setFixedWidth(180)
        self.setFixedHeight(28)
        self.setDigitCount(12)
        self.display('0.0')
