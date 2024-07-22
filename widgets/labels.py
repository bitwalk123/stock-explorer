import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from funcs.tide import conv_timestamp2date
from structs.res import AppRes


class DockImgTitle(QWidget):
    def __init__(self, name_image: str, title: str):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        lab_image = QLabel()
        lab_image.setContentsMargins(0, 0, 0, 0)
        res = AppRes()
        image = QPixmap(os.path.join(res.getImagePath(), name_image)).scaled(16, 16)
        lab_image.setPixmap(image)
        layout.addWidget(lab_image)

        lab_text = QLabel(title)
        lab_text.setStyleSheet('QLabel {font-size: small;}')
        layout.addWidget(lab_text)


class Label(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setContentsMargins(0, 0, 0, 0)


class LabelDateStr(QLabel):
    def __init__(self, dtdate: str, bcolor: str):
        super().__init__(dtdate)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("""
            QLabel{
                font-family: monospace;
                 background-color: %s;
            }
        """ % bcolor)


class LabelFlat(Label):
    def __init__(self, title: str):
        super().__init__(title)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("""
        QLabel {
            color: black;
            background-color: white;
            font-family: monospace;
        }
        """)


class LabelHeader(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet('QLabel {font-family: monospace;}')


class LabelLogo(QLabel):
    def __init__(self, logo: str):
        super().__init__()
        pixmap = QPixmap(logo).scaledToHeight(16)
        self.setPixmap(pixmap)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(2)


class LabelNewsDate(QLabel):
    def __init__(self, date: str):
        super().__init__()
        self.setText(date)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            background-color: white;
            font-family: monospace;
        }
        """)


class LabelNewsMsg(QLabel):
    def __init__(self, url: str, msg: str):
        super().__init__()
        self.setText('<a href="%s">%s</a>' % (url, msg))
        self.setOpenExternalLinks(False)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            background-color: white;
            font-family: monospace;
        }
        """)


class LabelStatus(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        QLabel {
            font-family: monospace;
        }
        """)


class LabelTicker(QLabel):
    def __init__(self, ticker: str, bcolor: str):
        super().__init__(ticker)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("""
            QLabel {
                padding-left: 0.1em;
                padding-right: 0.1em;
                font-family: monospace;
                background-color: %s;
            }
        """ % bcolor)


class LabelTitle(Label):
    def __init__(self, title: str):
        super().__init__(title)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            color: #444;
            background-color: #eee;
            font-family: monospace;
            padding-left: 0.5em;
        }
        """)


class LabelValue(Label):
    def __init__(self):
        super().__init__(title='')
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            color: #222;
            background-color: white;
            font-family: monospace;
        }
        """)

    def setValue(self, value):
        value_str = str(value)
        self.setText(value_str)


class LabelDate(LabelValue):
    def __init__(self):
        super().__init__()
        self.timestamp = 0

    def setDate(self, timestamp):
        self.timestamp = timestamp
        date = conv_timestamp2date(timestamp)
        self.setText(str(date))


class LabelValueStr(QLabel):
    def __init__(self, value_str: str, bcolor: str):
        super().__init__(value_str)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("""
            QLabel{
                font-family: monospace;
                background-color: %s;
            }
        """ % bcolor)
