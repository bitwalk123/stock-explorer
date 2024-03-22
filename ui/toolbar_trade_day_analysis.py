import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QMainWindow,
    QToolButton,
)

from funcs.tide import get_ymd
from structs.day_trade import DayTrade
from structs.res import AppRes
from widgets.entries import EntryDate, EntryTicker
from widgets.labels import Label
from widgets.pads import HPad
from widgets.toolbar_main import ToolBarMain


class ToolBarTradeDayAnalysis(ToolBarMain):
    drawRequested = Signal(DayTrade)

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.calendar = None
        self.parent = parent
        self.res = res = AppRes()

        # Ticker
        lab_ticker = Label('銘柄')
        lab_ticker.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_ticker)

        self.ent_ticker = ent_ticker = EntryTicker()
        self.addWidget(ent_ticker)
        self.addSeparator()

        but_bookmark = QToolButton()
        but_bookmark.setContentsMargins(0, 0, 0, 0)
        icon_bookmark = QIcon(os.path.join(res.getImagePath(), 'bookmark.png'))
        but_bookmark.setIcon(icon_bookmark)
        # but_bookmark.clicked.connect()
        self.addWidget(but_bookmark)

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

        self.addSeparator()

        self.combo_interval = combo_interval = QComboBox()
        combo_interval.setContentsMargins(0, 0, 0, 0)
        intervals = ['１分足']
        combo_interval.addItems(intervals)
        combo_interval.setCurrentText(intervals[0])
        self.addWidget(combo_interval)

        self.addSeparator()

        but_chart = QToolButton()
        but_chart.setContentsMargins(0, 0, 0, 0)
        but_chart.setToolTip('チャートをプロット')
        icon_chart = QIcon(os.path.join(res.getImagePath(), 'chart.png'))
        but_chart.setIcon(icon_chart)
        but_chart.clicked.connect(self.on_draw_chart)
        self.addWidget(but_chart)

        pad = HPad()
        self.addWidget(pad)

    def on_select_calendar(self):
        self.calendar = calendar = QCalendarWidget()
        calendar.setMaximumDate(QDate(*get_ymd()))
        date = self.ent_date.getDate()
        if date is not None:
            calendar.setSelectedDate(date)
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
        interval = self.combo_interval.currentText()

        info = DayTrade()
        info.code = code
        info.start = start
        info.end = end
        info.interval = interval
        info.jpx = False
        self.drawRequested.emit(info)
