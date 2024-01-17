import datetime as dt
import mplfinance as mpf
import yfinance as yf

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from funcs.tbl_ticker import get_cname_with_code
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_analytics import ToolBarNavigation
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainAnalytics(TabPanelMain):
    tab_label = '分析'
    resizeRequested = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)

        self.toolbar = None
        self.dock_bottom = None
        self.res = AppRes()

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarNavigation(self)
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
        ticker = '%s.T' % code
        df = yf.download(ticker, start, end, interval='5m')

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
