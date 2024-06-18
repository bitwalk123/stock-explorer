from PySide6.QtWidgets import QStatusBar

from widgets.labels import LabelStatus


class DTAStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.status = LabelStatus()
        self.addWidget(self.status)

    def setStatusMSG(self, msg: str):
        self.status.setText(msg)
