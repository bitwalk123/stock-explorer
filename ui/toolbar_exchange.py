import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QToolButton

from funcs.tide import get_past_date
from structs.res import AppRes
from widgets.combos import ComboTradeRange
from widgets.entries import EntryTicker
from widgets.labels import Label
from widgets.pads import HPad
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain


class ToolBarExchange(ToolBarMain):
    periodUpdate = Signal()

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.parent = parent
        self.res = res = AppRes()

        # Ticker
        lab_currency = Label('為替')
        lab_currency.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_currency)

        self.ent_currency = ent_currency = EntryTicker()
        ent_currency.setEnabled(False)
        """
        ent_currency.returnPressed.connect(
            self.on_currency_entered
        )
        """
        self.addWidget(ent_currency)

        lab_range = Label('期間')
        lab_range.setContentsMargins(10, 0, 5, 0)
        self.addWidget(lab_range)

        self.combo_range = combo_range = ComboTradeRange()
        # combo_range.setEnabled(False)
        combo_range.currentIndexChanged.connect(
            self.on_selected_range_changed
        )
        self.addWidget(combo_range)

        self.addSeparator()

        but_up = QToolButton()
        but_up.setContentsMargins(0, 0, 0, 0)
        but_up.setToolTip('前のコード')
        icon_up = QIcon(os.path.join(res.getImagePath(), 'arrow_up.png'))
        but_up.setIcon(icon_up)
        but_up.setEnabled(False)
        # but_up.clicked.connect(self.on_currency_up)
        self.addWidget(but_up)
        # Shortcut
        key_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        # key_up.activated.connect(self.on_currency_up)

        # Go down ticker
        but_down = QToolButton()
        but_down.setContentsMargins(0, 0, 0, 0)
        but_down.setToolTip('次のコード')
        icon_down = QIcon(os.path.join(res.getImagePath(), 'arrow_down.png'))
        but_down.setIcon(icon_down)
        but_down.setEnabled(False)
        # but_down.clicked.connect(self.on_currency_down)
        self.addWidget(but_down)
        # Shortcut
        key_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        # key_down.activated.connect(self.on_currency_down)

        # Separator
        hpad = HPad()
        self.addWidget(hpad)

    def getPlotType(self) -> str:
        return 'exchange'

    def getStartDate(self):
        sel = self.combo_range.currentText()
        return get_past_date(sel)

    def on_selected_range_changed(self):
        self.periodUpdate.emit()

    def updateCurrency(self, currency: str):
        self.ent_currency.setText(currency)
