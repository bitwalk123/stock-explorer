from PySide6.QtWidgets import QLabel, QFrame


class LabelFlat(QLabel):

    def __init__(self, title: str):
        super().__init__(title)
        self.setContentsMargins(0, 0, 5, 0)
        self.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
        self.setLineWidth(2)
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
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
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
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setStyleSheet("""
        QLabel {
            color: #222;
            background-color: white;
            font-family: monospace;
        }
        """)
