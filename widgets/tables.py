from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPlainTextEdit,
)


class CellDescription(QPlainTextEdit):
    def __init__(self, value):
        super().__init__(str(value))
        self.setStyleSheet('QPlainTextEdit {padding:0 2px;}')


class CellGeneral(QLabel):
    def __init__(self, value):
        super().__init__(str(value))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet('QLabel {padding:0 2px;}')


class CellHyperLink(QLabel):
    def __init__(self, url: str):
        super().__init__()
        self.setText('<a href="%s">%s</a>' % (url, url))
        self.setOpenExternalLinks(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet('QLabel {padding:0 2px;}')


class HeaderTickerInfo(QLabel):
    def __init__(self, value_str: str):
        super().__init__(value_str)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setStyleSheet('QLabel {padding:0 2px;}')
