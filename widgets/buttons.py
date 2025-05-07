from PySide6.QtWidgets import QPushButton, QToolButton


class Button(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QPushButton {font-family: monospace;}')

class ToolButton(QToolButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QToolButton {font-family: monospace;}')

