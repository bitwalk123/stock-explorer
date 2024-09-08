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

from structs.res import AppRes
from widgets.charts import ChartExchange


class DayTrendAnalyzerExchange(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ticker = yf.Ticker('USDJPY=X')

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'budget.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('為替レート')
        self.setFixedSize(400, 400)

        self.chart = chart = ChartExchange()
        self.setCentralWidget(chart)
        self.draw_chart()

        timer = QTimer(self)
        timer.timeout.connect(self.draw_chart)
        timer.start(20000)

    def draw_chart(self):
        df = self.get_exchange()
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
        title = '%.3f JPY at %s' % (df0['Close'].iloc[0], str(df0.index[0].time()))
        self.chart.ax.set_title(title)

        self.chart.ax.set_ylabel('USD - JPY')
        self.chart.ax.grid()
        self.chart.refreshDraw()

    def get_exchange(self) -> pd.DataFrame:
        end = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
        delta = dt.timedelta(hours=3)
        start = end - delta

        df = self.ticker.history(start=start, end=end, interval='1m')
        if len(df) > 0:
            df.index = df.index.tz_convert('Asia/Tokyo')

        return df

    def on_update(self):
        self.draw_chart()


def main():
    app = QApplication()
    ex = DayTrendAnalyzerExchange()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
