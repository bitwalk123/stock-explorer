from PySide6.QtWidgets import QDockWidget, QVBoxLayout, QPushButton, QScrollArea, QWidget, QSizePolicy, QLabel


class DockTicker(QDockWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        area = QScrollArea()
        area.setContentsMargins(0, 0, 0, 0)
        area.setWidgetResizable(True)
        self.setWidget(area)

        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        base.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        area.setWidget(base)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        base.setLayout(layout)
        for i in range(1000):
            but = QPushButton(str(i))
            but.setContentsMargins(0, 0, 0, 0)
            but.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            layout.addWidget(but)