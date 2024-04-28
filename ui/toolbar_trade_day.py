import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QToolButton,
    QToolTip,
)

from funcs.tbl_ticker import get_cname_with_code
from funcs.tide import get_ymd
from structs.day_trade import DayTrade
from structs.res import AppRes
from widgets.buttons import JPXCheckBox
from widgets.combos import ComboBookmarkAll
from widgets.entries import EntryDate, EntryTicker
from widgets.labels import Label
from widgets.pads import HPad
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain


class ToolBarTradeDay(ToolBarMain):
    drawRequested = Signal(DayTrade)
    resizeRequested = Signal(bool)

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

        # JPX or not
        self.chk_jpx = JPXCheckBox()
        self.addWidget(self.chk_jpx)

        # Bookmark for Ticker
        self.combo_bookmark = ComboBookmarkAll()
        self.combo_bookmark.currentIndexChanged.connect(self.on_bookmark_updated)
        self.addWidget(self.combo_bookmark)

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
        but_calendar.clicked.connect(self.on_calendar_selected)
        self.addWidget(but_calendar)

        self.addSeparator()

        self.combo_interval = combo_interval = QComboBox()
        combo_interval.setContentsMargins(0, 0, 0, 0)
        intervals = ['１分足', '５分足']
        combo_interval.addItems(intervals)
        combo_interval.setCurrentText(intervals[1])
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

        but_resize = QToolButton()
        but_resize.setContentsMargins(0, 0, 0, 0)
        icon_resize = QIcon(os.path.join(res.getImagePath(), 'resize.png'))
        but_resize.setIcon(icon_resize)
        but_resize.setCheckable(True)
        but_resize.toggled.connect(self.on_resize_toggled)
        self.addWidget(but_resize)

        # INIT
        idx = self.combo_bookmark.currentIndex()
        self.on_bookmark_updated(idx)

    def isJPX(self) -> bool:
        return self.chk_jpx.isChecked()

    def on_activated(self, date_start: QDate):
        self.ent_date.setDate(date_start)

        calendar: QCalendarWidget = self.sender()
        calendar.hide()
        calendar.deleteLater()

    def on_bookmark_updated(self, idx: int):
        self.ent_ticker.setText(self.combo_bookmark.getTicker(idx))
        self.chk_jpx.setChecked(self.combo_bookmark.isJPX(idx))

    def on_calendar_selected(self):
        self.calendar = calendar = QCalendarWidget()
        calendar.setMaximumDate(QDate(*get_ymd()))
        date = self.ent_date.getDate()
        if date is not None:
            calendar.setSelectedDate(date)
        calendar.activated.connect(self.on_activated)
        calendar.show()

    def on_draw_chart(self):
        code = self.ent_ticker.text()
        start, end = self.ent_date.getDateRange()
        interval = self.combo_interval.currentText()

        info = DayTrade()
        info.code = code
        info.start = start
        info.end = end
        info.interval = interval
        info.jpx = self.isJPX()
        self.drawRequested.emit(info)

    def on_resize_toggled(self, checked: bool):
        self.resizeRequested.emit(checked)

    def on_ticker_entered(self):
        code = self.ent_ticker.text()
        cname = get_cname_with_code(code)
        self.ent_ticker.setToolTip(cname)
        if cname != '':
            QToolTip.showText(
                self.ent_ticker.pos(),
                self.ent_ticker.toolTip()
            )
