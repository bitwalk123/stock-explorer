from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout


class GridLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

