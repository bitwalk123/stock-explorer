from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setTextVisible(True)
        self.setMaximum(100)  # プログレスバーの最大値を100に設定
        self.setValue(0)  # 初期値は0
