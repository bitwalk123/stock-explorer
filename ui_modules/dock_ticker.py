from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QDockWidget,
    QRadioButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from functions.get_list_ticker import get_list_ticker


class DockTicker(QDockWidget):
    """Dock for listing all tickers
    """
    clicked = Signal(int)

    def __init__(self):
        super().__init__()
        self.setTitleBarWidget(QWidget(None))
        # self.setContentsMargins(0, 0, 0, 0)

        self.id_max = 0
        self.area = QScrollArea()
        self.rb_group = QButtonGroup()
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        #self.area.setContentsMargins(0, 0, 0, 0)
        self.area.setWidgetResizable(True)
        self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.area)

        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        self.area.setWidget(base)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        # layout.setContentsMargins(5, 0, 5, 0)
        base.setLayout(layout)

        id = 0
        dict_ticker = get_list_ticker()
        for key in dict_ticker.keys():
            rb = QRadioButton(str(key))
            self.rb_group.addButton(rb)
            self.rb_group.setId(rb, id)
            id += 1
            # rb.setContentsMargins(0, 0, 0, 0)
            rb.setToolTip(dict_ticker[key])
            rb.toggled.connect(self.on_button_clicked)
            layout.addWidget(rb)
        self.id_max = id

    def on_button_clicked(self):
        """Handling for button click
        """
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            self.area.ensureWidgetVisible(rb)
            code = int(rb.text())
            self.clicked.emit(code)

    def get_first_button(self) -> Union[QAbstractButton, None]:
        """Get first radio button
        """
        if len(self.rb_group.buttons()) > 0:
            return self.rb_group.buttons()[0]
        else:
            return None

    def get_current_ticker(self) -> Union[int, None]:
        """Get current ticler selected
        """
        rb = self.rb_group.checkedButton()
        if rb is not None:
            return int(rb.text())
        else:
            return None

    def get_ticker_down(self):
        id = self.rb_group.checkedId()
        if id < len(self.rb_group.buttons()) - 1:
            id_new = id + 1
        else:
            id_new = id
        rb = self.rb_group.button(id_new)
        rb.setChecked(True)

    def get_ticker_up(self):
        id = self.rb_group.checkedId()
        if id > 0:
            id_new = id - 1
        else:
            id_new = id
        rb = self.rb_group.button(id_new)
        rb.setChecked(True)
