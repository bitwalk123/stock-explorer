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

        self.id_max = 0
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
        id = 0
        for key in dict_ticker.keys():
            rb = QRadioButton(str(key))
            self.rb_group.addButton(rb)
            self.rb_group.setId(rb, id)
            id += 1
            rb.setContentsMargins(0, 0, 0, 0)
            # rb.setStyleSheet('padding-left:5px;')
            rb.setToolTip(dict_ticker[key])
            # but.setSizePolicy(
            #    QSizePolicy.Policy.Expanding,
            #    QSizePolicy.Policy.Fixed
            # )
            rb.toggled.connect(self.on_button_clicked)
            layout.addWidget(rb)
        self.id_max = id

    def on_button_clicked(self):
        """handling for button click
        """
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            code = int(rb.text())
            self.clicked.emit(code)

    def get_first_button(self) -> QAbstractButton:
        return self.rb_group.buttons()[0]

    def get_current_ticker(self):
        rb = self.rb_group.checkedButton()
        print(self.rb_group.id(rb))
        return (rb.text())
