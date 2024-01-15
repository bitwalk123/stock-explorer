import datetime as dt
import mplfinance as mpf
import yfinance as yf

from PySide6.QtCore import Qt

from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_analytics import ToolBarNavigation
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainAnalytics(TabPanelMain):
    tab_label = '分析'

    def __init__(self, parent):
        super().__init__(parent)

        self.toolbar = None
        self.dock_bottom = None
        self.res = AppRes()

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarNavigation(self)
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


    def draw(self):
        chart = self.centralWidget()

        d = 12
        start = dt.date(2024, 1, d)
        end = dt.date(2024, 1, d + 1)
        ticker = '8035.T'  # 東京エレクトロン
        df = yf.download(ticker, start, end, interval='5m')
        # mpf.plot(df, type='candle', style='binance', figratio=(12, 4))
        mpf.plot(
            df,
            type='candle',
            datetime_format='%H:%M',
            tight_layout=False,
            style=self.res.getCandleStyle(),
            ax=chart.ax
        )
        chart.ax.set_ylabel('Price (JPY)')
        chart.ax.yaxis.tick_right()
        chart.ax.yaxis.set_label_position('right')
        chart.ax.grid()
        chart.refreshDraw()
