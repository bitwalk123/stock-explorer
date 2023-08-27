from PySide6.QtWidgets import QLabel, QFrame

from functions.conv_timestamp2date import conv_timestamp2date


class LabelFlat(QLabel):

    def __init__(self, title: str):
        super().__init__(title)
        self.setContentsMargins(0, 0, 5, 0)
        # self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("""
        QLabel {
            color: black;
            background-color: white;
            font-family: monospace;
        }
        """)


class LabelTitle(QLabel):

    def __init__(self, title: str):
        super().__init__(title)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            color: #444;
            background-color: #eee;
            font-family: monospace;
        }
        """)


class LabelValue(QLabel):

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            color: #222;
            background-color: white;
            font-family: monospace;
        }
        """)


class LabelDate(LabelValue):

    def __init__(self):
        super().__init__()
        self.timestamp = 0

    def setDate(self, timestamp):
        self.timestamp = timestamp
        dt = conv_timestamp2date(timestamp)
        self.setText(str(dt))
