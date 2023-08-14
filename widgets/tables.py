from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)


class CellDescription(QPlainTextEdit):
    def __init__(self, value):
        super().__init__(str(value))
        self.setStyleSheet('QPlainTextEdit {padding:0 2px; background-color:white;}')
        self.setFixedHeight(200)


class CellGeneral(QLabel):
    def __init__(self, value):
        super().__init__(str(value))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet('QLabel {padding:0 2px; background-color:white;}')


class CellHyperLink(QLabel):
    def __init__(self, url: str):
        super().__init__()
        self.setText('<a href="%s">%s</a>' % (url, url))
        self.setOpenExternalLinks(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet('QLabel {padding:0 2px; background-color:white;}')


class CellOfficers(QScrollArea):
    def __init__(self, list_dict: list):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(200)

        base = QFrame()
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        base.setContentsMargins(0, 0, 0, 0)
        self.setWidget(base)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        base.setLayout(layout)

        for info in list_dict:
            frm = QFrame()
            frm.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
            frm.setLineWidth(2)
            frm.setStyleSheet('QFrame {background-color:#ccc;}')
            frm.setContentsMargins(2, 2, 2, 2)
            layout2 = QGridLayout()
            layout2.setContentsMargins(0, 0, 0, 0)
            layout2.setSpacing(0)
            frm.setLayout(layout2)

            row = 0
            for key in info.keys():
                lab_left = HeaderGeneral(key)
                lab_right = CellGeneral(info[key])
                lab_right.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Expanding
                )
                layout2.addWidget(lab_left, row, 0)
                layout2.addWidget(lab_right, row, 1)
                row += 1

            layout.addWidget(frm)


class HeaderGeneral(QLabel):
    def __init__(self, value_str: str):
        super().__init__(value_str)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setStyleSheet('QLabel {padding:0 2px; background-color:#f0f0f0;}')
