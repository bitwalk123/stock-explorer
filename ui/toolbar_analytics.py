import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QFrame, QLineEdit

from structs.res import AppRes
from widgets.entries import EntryTicker, EntryDate
from widgets.labels import Label
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain


class ToolBarNavigation(ToolBarMain):
    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.parent = parent
        self.res = res = AppRes()

        # Ticker
        lab_ticker = Label('銘柄')
        lab_ticker.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_ticker)

        self.ent_ticker = ent_ticker = EntryTicker()
        # ent_ticker.returnPressed.connect(
        #    self.on_ticker_entered
        # )
        self.addWidget(ent_ticker)

        ent_date = EntryDate()
        ent_date.setEnabled(False)
        ent_date.setContentsMargins(10, 0, 0, 0)
        self.addWidget(ent_date)

        but_calendar = QToolButton()
        but_calendar.setContentsMargins(0, 0, 0, 0)
        but_calendar.setToolTip('カレンダー')
        icon_up = QIcon(os.path.join(res.getImagePath(), 'calendar.png'))
        but_calendar.setIcon(icon_up)
        but_calendar.clicked.connect(self.on_select_calendar)
        self.addWidget(but_calendar)

    def on_select_calendar(self):
        pass