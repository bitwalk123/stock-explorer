from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget, QButtonGroup, QRadioButton, QAbstractButton,
)

from functions.get_list_ticker import get_list_ticker


class DockTicker(QDockWidget):
    """Dock for listing all tickers
    """
    clicked = Signal(int)

    def __init__(self):
        super().__init__()
        # self.setWindowTitle('コード')
        self.setContentsMargins(0, 0, 0, 0)
        self.rb_group = QButtonGroup()
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
            rb = QRadioButton(str(key))
            self.rb_group.addButton(rb)
            rb.setContentsMargins(0, 0, 0, 0)
            # rb.setStyleSheet('padding-left:5px;')
            rb.setToolTip(dict_ticker[key])
            # but.setSizePolicy(
            #    QSizePolicy.Policy.Expanding,
            #    QSizePolicy.Policy.Fixed
            # )
            rb.toggled.connect(self.on_button_clicked)
            layout.addWidget(rb)

    def on_button_clicked(self):
        """handling for button click
        """
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            code = int(rb.text())
            self.clicked.emit(code)

    def get_first_button(self) -> QAbstractButton:
        return self.rb_group.buttons()[0]
