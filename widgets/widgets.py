from PySide6.QtWidgets import QWidget, QSizePolicy


class HPad(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
