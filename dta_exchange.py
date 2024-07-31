import datetime as dt
import os

import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import mplfinance as mpf
import sys

import pandas as pd
import yfinance as yf
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from structs.res import AppRes
from ui.toolbar_dta import DTAExchangeToolBar
from widgets.charts import ChartExchange


class DayTrendAnalyzerExchange(QMainWindow):
    def __init__(self):
        super().__init__()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'budget.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DTA - Exchange')
        self.setFixedSize(1000, 400)

        toolbar = DTAExchangeToolBar()
        toolbar.clickedUpdate.connect(self.on_update)
        self.addToolBar(toolbar)

        self.chart = chart = ChartExchange()
        self.setCentralWidget(chart)
        self.draw_chart()

        timer = QTimer(self)
        timer.timeout.connect(self.draw_chart)
        timer.start(30000)

    def draw_chart(self):
        df = self.get_exchange()

        self.chart.clearAxes()
        mpf.plot(
            df,
            type='candle',
            style='binance',
            ax=self.chart.ax,
        )

        df0 = df.tail(1)
        title = '%.3f JPY at %s' % (df0['Close'].iloc[0], str(df0.index[0].time()))
        self.chart.ax.set_title(title)

        self.chart.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.chart.ax.set_ylabel('USD - JPY')
        self.chart.ax.grid()
        self.chart.refreshDraw()

    def get_exchange(self) -> pd.DataFrame:
        delta = dt.timedelta(days=1)
        end = dt.date.today() + delta
        start = end - 2 * delta

        ticker = 'USDJPY=X'
        df = yf.download(ticker, start, end, interval='1m')
        df.index = df.index.tz_convert('Asia/Tokyo')
        df1 = df.tail(6 * 60)
        # print(df1.tail(5)[['Open', 'High', 'Low', 'Close']])
        return df1

    def on_update(self):
        self.draw_chart()


def main():
    app = QApplication()
    ex = DayTrendAnalyzerExchange()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
