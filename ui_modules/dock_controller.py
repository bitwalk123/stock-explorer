from PySide6.QtWidgets import QDockWidget, QWidget


class DockController(QDockWidget):
    """Dock for controller
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        base = QWidget()
        self.setWidget(base)

