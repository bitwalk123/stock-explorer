import datetime as dt
import mplfinance as mpf
import numpy as np
import os
import pandas as pd
import sys
import yfinance as yf
from zoneinfo import ZoneInfo

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from funcs.parabolic import psar
from structs.res import AppRes
from widgets.charts import ChartTrade


def draw_chart(chart: ChartTrade, df: pd.DataFrame):
    chart.clearAxes()
    dict_psar = psar(df)
    print(dict_psar)
    apds = [
        mpf.make_addplot(
            dict_psar['bear'],
            type='scatter',
            marker='o',
            markersize=5,
            color='magenta',
            label='downtrend',
            ax=chart.ax,
        ),
        mpf.make_addplot(
            dict_psar['bull'],
            type='scatter',
            marker='o',
            markersize=5,
            color='darkcyan',
            label='uptrend',
            ax=chart.ax,
        ),
    ]

    mpf.plot(
        df,
        type='candle',
        style='binance',
        addplot=apds,
        xrotation=0,
        ax=chart.ax,
    )

    df_bottom = df.tail(1)
    title = '%.f JPY at %s' % (
        df_bottom['Close'].iloc[0],
        str(df_bottom.index[0].time())
    )
    chart.ax.set_title(title)

    chart.ax.set_ylabel('Price')
    chart.ax.grid()
    chart.refreshDraw()


class DayTrendAnalyzerTrade(QMainWindow):
    def __init__(self):
        super().__init__()
        symbol = '8035.T'
        self.ticker = yf.Ticker(symbol)

        dt_now = dt.datetime.now(ZoneInfo("Asia/Tokyo"))
        y = dt_now.year
        m = dt_now.month
        d = dt_now.day
        self.dt_start_1 = dt_start_1 = pd.to_datetime('%4d-%02d-%02d 09:00:00+09:00' % (y, m, d))
        self.dt_end_1 = dt_end_1 = pd.to_datetime('%4d-%02d-%02d 11:30:00+09:00' % (y, m, d))
        self.dt_start_2 = dt_start_2 = pd.to_datetime('%4d-%02d-%02d 12:30:00+09:00' % (y, m, d))
        self.dt_end_2 = dt_end_2 = pd.to_datetime('%4d-%02d-%02d 15:00:00+09:00' % (y, m, d))

        dt_list_0 = pd.date_range(dt_start_1, periods=360, freq='min')
        dt_list = dt_list_0[(dt_list_0 <= dt_end_1) | (dt_list_0 >= dt_start_2)]
        n = len(dt_list)
        self.df = pd.DataFrame(
            {
                'Open': [np.nan] * n,
                'High': [np.nan] * n,
                'Low': [np.nan] * n,
                'Close': [np.nan] * n,
                'Volume': [np.nan] * n,
                'Dividends': [np.nan] * n,
                'Stock Splits': [np.nan] * n,
            },
            index=dt_list,
        )
        self.df.index.name = 'Datetime'

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'chart.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(symbol)
        self.setFixedSize(1000, 400)

        self.chart = chart = ChartTrade()
        self.setCentralWidget(chart)
        # self.draw_chart()

        timer = QTimer(self)
        timer.timeout.connect(self.on_update)
        timer.start(60000)

    def get_dataframe(self) -> pd.DataFrame:
        df = self.ticker.history(period='1d', interval='1m')

        return df

    def on_update(self):
        dt_now = dt.datetime.now(ZoneInfo("Asia/Tokyo"))
        if dt_now < self.dt_start_1:
            print('before market starting @', dt_now)
            return

        df = self.get_dataframe()
        if len(df) == 0:
            return

        for t in df.index[(df.index <= self.dt_end_1) | (df.index >= self.dt_start_2)]:
            self.df.loc[t] = df.loc[t]

        draw_chart(self.chart, self.df)


def main():
    app = QApplication()
    ex = DayTrendAnalyzerTrade()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
