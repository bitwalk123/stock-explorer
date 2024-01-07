from PySide6.QtWidgets import QToolBar


class ToolBarMain(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContentsMargins(2, 0, 2, 0)
