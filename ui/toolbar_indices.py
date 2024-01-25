import os

from PySide6.QtCore import Signal, Qt, QUrl
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QIcon,
    QKeySequence,
    QShortcut,
)
from PySide6.QtWidgets import (
    QMenu,
    QToolButton, QMainWindow,
)

from funcs.tide import get_past_date
from structs.res import AppRes
from ui.browser import NewsGoodBad, RakutenRanking
from widgets.labels import Label
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain
from widgets.combos import ComboTradeRange
from widgets.entries import EntryTicker
from widgets.pads import HPad


class ToolBarIndices(ToolBarMain):
    periodUpdate = Signal()
    indexDown = Signal()
    indexEntered = Signal(str)
    indexUp = Signal()

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.parent = parent
        self.res = res = AppRes()

        # Ticker
        lab_index = Label('指数')
        lab_index.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_index)

        self.ent_index = ent_index = EntryTicker()
        ent_index.returnPressed.connect(
            self.on_ticker_entered
        )
        self.addWidget(ent_index)

        lab_range = Label('期間')
        lab_range.setContentsMargins(10, 0, 5, 0)
        self.addWidget(lab_range)

        self.combo_range = combo_range = ComboTradeRange()
        combo_range.currentIndexChanged.connect(
            self.on_selected_range_changed
        )
        self.addWidget(combo_range)

        self.addSeparator()

        but_up = QToolButton()
        but_up.setContentsMargins(0, 0, 0, 0)
        but_up.setToolTip('前の指数')
        icon_up = QIcon(os.path.join(res.getImagePath(), 'arrow_up.png'))
        but_up.setIcon(icon_up)
        but_up.clicked.connect(self.on_index_up)
        self.addWidget(but_up)
        # Shortcut
        key_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        key_up.activated.connect(self.on_index_up)

        # Go down ticker
        but_down = QToolButton()
        but_down.setContentsMargins(0, 0, 0, 0)
        but_down.setToolTip('次の指数')
        icon_down = QIcon(os.path.join(res.getImagePath(), 'arrow_down.png'))
        but_down.setIcon(icon_down)
        but_down.clicked.connect(self.on_index_down)
        self.addWidget(but_down)
        # Shortcut
        key_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        key_down.activated.connect(self.on_index_down)

    def getStartDate(self):
        sel = self.combo_range.currentText()
        return get_past_date(sel)

    def on_selected_range_changed(self):
        self.periodUpdate.emit()

    def on_index_down(self):
        self.indexDown.emit()

    def on_ticker_entered(self):
        entered: str = self.ent_index.text()
        self.indexEntered.emit(entered)

    def on_index_up(self):
        self.indexUp.emit()

    def updateiTicker(self, iticker: str):
        self.ent_index.setText(iticker)
