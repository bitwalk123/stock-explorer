from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from database.get_list_ticker import get_list_ticker


class DockTicker(QDockWidget):
    """Dock for listing all tickers
    """
    clicked = Signal(int)

    def __init__(self):
        super().__init__()
        # self.setWindowTitle('コード')
        self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        area = QScrollArea()
        area.setContentsMargins(0, 0, 0, 0)
        area.setWidgetResizable(True)
        # area.setSizePolicy(
        #    QSizePolicy.Policy.Expanding,
        #    QSizePolicy.Policy.Expanding
        # )
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(area)

        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        # base.setSizePolicy(
        #    QSizePolicy.Policy.Expanding,
        #    QSizePolicy.Policy.Expanding
        # )
        area.setWidget(base)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        base.setLayout(layout)

        dict_ticker = get_list_ticker()
        for key in dict_ticker.keys():
            but = QPushButton(str(key))
            but.setContentsMargins(0, 0, 0, 0)
            but.setStyleSheet('text-align:left;padding-left:5px;')
            but.setToolTip(dict_ticker[key])
            # but.setSizePolicy(
            #    QSizePolicy.Policy.Expanding,
            #    QSizePolicy.Policy.Fixed
            # )
            but.clicked.connect(self.on_button_clicked)
            layout.addWidget(but)

    def on_button_clicked(self):
        """handling for button click
        """
        but: QPushButton = self.sender()
        code = int(but.text())
        self.clicked.emit(code)
