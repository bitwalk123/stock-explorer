import pandas as pd

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from widgets.models import TblPredictModel


class CellDescription(QPlainTextEdit):
    def __init__(self, value):
        super().__init__(str(value))
        self.setFixedHeight(200)
        self.setStyleSheet(
            """
            QPlainTextEdit {
                padding: 0 2px;
                background-color: white;
            }
            """
        )


class CellGeneral(QLabel):
    def __init__(self, value):
        super().__init__(str(value))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet(
            """
            QLabel {
                padding: 0 2px;
                background-color: white;
            }
            """
        )


class CellHyperLink(QLabel):
    def __init__(self, url: str):
        super().__init__()
        self.setText('<a href="%s">%s</a>' % (url, url))
        self.setOpenExternalLinks(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet(
            """
            QLabel {
                padding: 0 2px;
                background-color: white;
            }
            """
        )


class CellOfficers(QScrollArea):
    def __init__(self, list_dict: list):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # if len(list_dict) > 1:
        #    self.setFixedHeight(200)
        # else:
        #    self.setFixedHeight(120)
        self.setFixedHeight(200)

        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        self.setWidget(base)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        base.setLayout(layout)

        for info in list_dict:
            frm = CellOfficerSingle(info)
            layout.addWidget(frm)


class CellOfficerSingle(QFrame):
    def __init__(self, info: dict):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(2)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #ccc;
            }
            """
        )
        self.setContentsMargins(2, 2, 2, 2)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        row = 0
        for key in info.keys():
            lab_left = HeaderGeneral(key)
            lab_right = CellGeneral(info[key])
            lab_right.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )
            layout.addWidget(lab_left, row, 0)
            layout.addWidget(lab_right, row, 1)
            row += 1


class HeaderGeneral(QLabel):
    def __init__(self, value_str: str):
        super().__init__(value_str)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setStyleSheet(
            """
            QLabel {
                padding: 0 2px;
                background-color: #f0f0f0;
            }
            """
        )


class TblPredict(QTableView):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.setStyleSheet(
            """
            QTableView {
                font-family: monospace;
            }
            """
        )
        self.setAlternatingRowColors(True)
        self.model = TblPredictModel(df)
        self.setModel(self.model)
        header_vert = self.horizontalHeader()
        header_vert.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

    def get_code(self, row: int) -> int:
        code = int(self.model.get_row(row)['コード'].iloc[0])
        return code
