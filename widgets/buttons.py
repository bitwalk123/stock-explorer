from PySide6.QtWidgets import QPushButton


class TickerButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCheckable(True)
        self.setContentsMargins(0, 0, 0, 0)
