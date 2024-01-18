import datetime as dt
import re

import mplfinance as mpf

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from funcs.tbl_ticker import get_cname_with_code, get_id_code_from_code
from funcs.tbl_trade import get_max_date_from_trade_with_id_code_less_date
from funcs.tbl_trade5m import refresh_trade5m
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade5m import ToolBarTrade5m
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainTrade5m(TabPanelMain):
    tab_label = '５分足チャート'
    resizeRequested = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)

        self.toolbar = None
        self.dock_bottom = None
        self.res = AppRes()

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarTrade5m(self)
        toolbar.drawRequested.connect(self.on_draw)
        toolbar.resizeRequested.connect(self.on_resize_requested)
        self.addToolBar(toolbar)

        # CandleStick chart as default
        chart = Trend(gtype='Trend')
        self.setCentralWidget(chart)

        # Bottom Dock
        self.dock_bottom = dock_bottom = DockNavigator(self, chart)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )

    def on_draw(self, code: str, start: str, end: str):
        pattern = re.compile(r'^([0-9]+)-([0-9]+)-([0-9]+)$')
        m = pattern.match(start)
        if m:
            yyyy = int(m.group(1))
            mm = int(m.group(2))
            dd = int(m.group(3))
            start_dt = dt.datetime(yyyy, mm, dd)
            print(start_dt)
            start_timestamp = int(start_dt.timestamp())
            print(start_timestamp)
            id_code = get_id_code_from_code(code)
            print(id_code)
            prev_timestamp = get_max_date_from_trade_with_id_code_less_date(id_code, start_timestamp)
            print(prev_timestamp)
            # Need to get Close price of precious trade day

        df = refresh_trade5m(code, start, end)

        cname = get_cname_with_code(code)
        title = '%s (%s)\n５分足チャート on %s' % (cname, code, start)

        chart: QWidget | Trend = self.centralWidget()
        chart.clearAxes()
        mpf.plot(
            df,
            type='candle',
            datetime_format='%H:%M',
            tight_layout=False,
            style=self.res.getCandleStyle(),
            ax=chart.ax
        )
        chart.ax.set_title(title)
        chart.ax.set_ylabel('Price (JPY)')
        chart.ax.yaxis.tick_right()
        chart.ax.yaxis.set_label_position('right')
        chart.ax.grid()
        chart.refreshDraw()

    def on_resize_requested(self, flag: bool):
        self.resizeRequested.emit(flag)
