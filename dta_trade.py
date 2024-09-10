import datetime as dt
import os

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

from base.psar import PSAR
from structs.res import AppRes
from widgets.charts import ChartTrade


class DayTrendAnalyzerTrade(QMainWindow):
    def __init__(self):
        super().__init__()
        symbol = '8035.T'
        self.ticker = yf.Ticker(symbol)

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'chart.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(symbol)
        self.setFixedSize(1000, 400)

        self.chart = chart = ChartTrade()
        self.setCentralWidget(chart)
        self.draw_chart()

        timer = QTimer(self)
        timer.timeout.connect(self.draw_chart)
        timer.start(60000)

    def draw_chart(self):
        df = self.get_dataframe()
        if len(df) == 0:
            return

        self.chart.clearAxes()
        mpf.plot(
            df,
            type='candle',
            style='binance',
            ax=self.chart.ax,
        )

        df0 = df.tail(1)
        title = '%f JPY at %s' % (df0['Close'].iloc[0], str(df0.index[0].time()))
        self.chart.ax.set_title(title)

        self.chart.ax.set_ylabel('Price')
        self.chart.ax.grid()
        self.chart.refreshDraw()

    def get_dataframe(self) -> pd.DataFrame:
        end = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
        delta = dt.timedelta(hours=6)
        start = end - delta

        df = self.ticker.history(start=start, end=end, interval='1m')
        if len(df) > 0:
            df.index = df.index.tz_convert('Asia/Tokyo')

        return df

    def on_update(self):
        self.draw_chart()


def main():
    app = QApplication()
    ex = DayTrendAnalyzerTrade()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
