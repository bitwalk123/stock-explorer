import os

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QStyle,
    QToolBar,
)

from structs.res import AppRes


class ToolBarTrading(QToolBar):
    Back = Signal()
    Forward = Signal()
    Load = Signal(str)
    Source = Signal()

    def __init__(self):
        super().__init__()
        res = AppRes()

        but_back = QPushButton()
        icon_back = self.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowBack
        )
        but_back.setIcon(icon_back)
        but_back.clicked.connect(self.back)
        self.addWidget(but_back)

        but_forward = QPushButton()
        icon_forward = self.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowForward
        )
        but_forward.setIcon(icon_forward)
        but_forward.clicked.connect(self.forward)
        self.addWidget(but_forward)

        self.address = address = QLineEdit()
        address.setStyleSheet("""
            QLineEdit{background-color: white;}
        """)
        address.returnPressed.connect(self.load)
        self.addWidget(address)

        but_source = QPushButton()
        icon_source = QIcon(os.path.join(res.getImagePath(), 'html.png'))
        but_source.setIcon(icon_source)
        but_source.clicked.connect(self.source)
        self.addWidget(but_source)

    def back(self):
        self.Back.emit()

    def forward(self):
        self.Forward.emit()

    def load(self):
        lineedit: QLineEdit = self.sender()
        self.Load.emit(lineedit.text())

    def source(self):
        self.Source.emit()

    def setURL(self, url: QUrl):
        self.address.setText(url.toString())
