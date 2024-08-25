from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableView, QHeaderView, QAbstractButton, QVBoxLayout, QLabel


class TableView(QTableView):
    def __init__(self, label: str):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.label = label

        # Horizontal header of table
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Row colors
        self.setAlternatingRowColors(True)

    def getLabel(self) -> str:
        return self.label

def add_label(but: QAbstractButton):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    but.setLayout(layout)
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)
    return label


class PandasTableView(QTableView):
    __version__ = '0.0.1'

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTableView{
                font-family: monospace;
            }
            QTableCornerButton::section{
                border-width: 1px;
                border-color: #BABABA;
                border-style: outset;
            }
        """)
        but: Union[object, QAbstractButton] = self.findChild(QAbstractButton, '')
        if type(but) is QAbstractButton:
            self.label = add_label(but)
        else:
            self.label = None

    def setUpperLeftCornerTitle(self, title: str):
        if self.label is not None:
            self.label.setText(title)
