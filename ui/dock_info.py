from PySide6.QtWidgets import QDockWidget


class DockInfo(QDockWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setContentsMargins(0, 0, 0, 0)
