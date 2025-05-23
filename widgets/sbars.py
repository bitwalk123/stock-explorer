from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QStatusBar, QLabel

from widgets.pbars import ProgressBar


class StatusBarDebug(QStatusBar):
    def __init__(self):
        super().__init__()
        self.pbar = pbar = ProgressBar()
        self.addPermanentWidget(pbar)  # 永続的に表示
        self.lab_status = lab_status = QLabel('準備完了')
        self.lab_status.setContentsMargins(QMargins(5, 0, 0, 0))
        self.lab_status.setStyleSheet("""
            QLabel {
                font-size: 8pt;
            }
        """)
        self.addWidget(lab_status)

    def setText(self, msg: str):
        self.lab_status.setText(msg)

    def setValue(self, x: int):
        self.pbar.setValue(x)  # エラー時はプログレスバーをリセット
