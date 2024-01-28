import mplfinance as mpf

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from funcs.tbl_ticker import get_cname_with_code
from funcs.tbl_trade import get_previous_close
from funcs.tbl_trade_day import get_day_trade
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade_day import ToolBarTradeDay
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainTradeDay(TabPanelMain):
    tab_label = 'チャート（当日）'
    resizeRequested = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)

        self.toolbar = None
        self.dock_bottom = None
        self.res = AppRes()

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarTradeDay(self)
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

    def on_draw(self, code: str, start: str, end: str, str_interval: str):
        close_prev = get_previous_close(code, start)
        if str_interval == '１分足':
            interval = '1m'
        elif str_interval == '５分足':
            interval = '5m'
        else:
            interval = ''
        df = get_day_trade(code, start, end, interval)

        cname = get_cname_with_code(code)
        title = '%s (%s)\n%sチャート on %s' % (cname, code, str_interval, start)

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
        if type(close_prev) is not None:
            chart.ax.axhline(
                y=close_prev,
                color='r',
                linewidth=1,
                linestyle=':',
                xmax=0.25
            )

        chart.ax.set_title(title)
        chart.ax.set_ylabel('Price (JPY)')
        chart.ax.yaxis.set_tick_params(labelright=True)
        chart.ax.grid()
        chart.refreshDraw()

    def on_resize_requested(self, flag: bool):
        self.resizeRequested.emit(flag)
