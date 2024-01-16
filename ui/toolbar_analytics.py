import datetime as dt
import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QToolButton,
)

from funcs.tbl_ticker import get_cname_with_code
from funcs.tide import get_ymd
from structs.res import AppRes
from widgets.entries import (
    EntryDate,
    EntryTicker,
)
from widgets.labels import Label
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain


class ToolBarNavigation(ToolBarMain):
    drawRequested = Signal(str, str, str)

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.calendar = None
        self.parent = parent
        self.res = res = AppRes()

        # Ticker
        lab_ticker = Label('銘柄')
        lab_ticker.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_ticker)

        self.ent_ticker = ent_ticker = EntryTicker()
        ent_ticker.returnPressed.connect(self.on_ticker_entered)
        self.addWidget(ent_ticker)

        self.addSeparator()

        self.ent_date = ent_date = EntryDate()
        ent_date.setEnabled(False)
        ent_date.setContentsMargins(0, 0, 0, 0)
        self.addWidget(ent_date)

        but_calendar = QToolButton()
        but_calendar.setContentsMargins(0, 0, 0, 0)
        but_calendar.setToolTip('カレンダー')
        icon_calendar = QIcon(os.path.join(res.getImagePath(), 'calendar.png'))
        but_calendar.setIcon(icon_calendar)
        but_calendar.clicked.connect(self.on_select_calendar)
        self.addWidget(but_calendar)

        but_chart = QToolButton()
        but_chart.setContentsMargins(0, 0, 0, 0)
        but_chart.setToolTip('チャートをプロット')
        icon_chart = QIcon(os.path.join(res.getImagePath(), 'chart.png'))
        but_chart.setIcon(icon_chart)
        but_chart.clicked.connect(self.on_draw_chart)
        self.addWidget(but_chart)

    def on_select_calendar(self):
        self.calendar = calendar = QCalendarWidget()
        calendar.setMaximumDate(QDate(*get_ymd()))
        calendar.activated.connect(self.on_activated)
        calendar.show()

    def on_activated(self, date_start: QDate):
        self.ent_date.setDate(date_start)

        calendar: QCalendarWidget = self.sender()
        calendar.hide()
        calendar.deleteLater()

    def on_draw_chart(self):
        code = self.ent_ticker.text()
        start, end = self.ent_date.getDateRange()
        self.drawRequested.emit(code, start, end)

    def on_ticker_entered(self):
        code = self.ent_ticker.text()
        cname = get_cname_with_code(code)
        self.ent_ticker.setToolTip(cname)
