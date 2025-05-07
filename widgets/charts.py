import datetime
import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import yfinance as yf

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from funcs.plots import (
    clear_axes,
    draw_grid,
    refresh_draw, get_chart_title,
)
from structs.res import AppRes
from widgets.dialogs import DialogError


class CandleStick(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        # 　過去 1 年分のデータの分離用
        self.tdelta_1y = datetime.timedelta(days=366)
        # for Bollinger bands
        self.period = 20

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = dict()
        n = 2

        if n > 1:
            gs = self.fig.add_gridspec(
                n, 1,
                wspace=0.0, hspace=0.0,
                height_ratios=[3 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex='col')):
                self.ax[i] = axis
        else:
            self.ax[0] = self.fig.add_subplot(111)

        self.fig.subplots_adjust(left=0.075, right=0.995, top=0.95, bottom=0.06)

    def plot(self, ticker: yf.Ticker):
        """
        ローソク足チャートのプロット
        :param ticker:
        :return:
        """

        try:
            # 日足で過去 2 年分のデータを取得
            df0: pd.DataFrame = ticker.history(period='2y', interval='1d')
        except Exception as e:
            list_msg = list()
            for msg in e.args:
                list_msg.append(msg)
            dlg = DialogError('\n'.join(list_msg))
            dlg.exec()
            return

        # ローソク足のチャートには、そのうち過去 1 年分のみ使用する
        dt_last = df0.index[len(df0) - 1]
        df = df0[dt_last - self.tdelta_1y <= df0.index]

        apds = list()
        ax0 = self.ax[0]
        list_dt = df.index

        # Robust Bollinger bands
        self.add_robust_bollinger(apds, ax0, df0, list_dt)

        # 消去
        clear_axes(self.fig)

        mpf.plot(
            df,
            type='candle',
            style='default',
            volume=self.ax[1],
            addplot=apds,
            datetime_format='%y-%m-%d',
            xrotation=0,
            ax=self.ax[0],
        )

        y_lower, y_upper = self.ax[0].get_ylim()
        if y_lower < 0:
            self.ax[0].set_ylim(0, y_upper)

        # グリッド線
        draw_grid(self.fig)

        # 凡例
        self.ax[0].legend(loc='best', fontsize=8)

        # チャート・タイトル
        title = get_chart_title(ticker)
        self.ax[0].set_title(title)

        # 再描画
        refresh_draw(self.fig)

    def add_robust_bollinger(self, apds, ax, df, list_dt):
        """
        Robust Bollinger bands
        :param apds:
        :param ax:
        :param df:
        :param list_dt:
        :return:
        """
        mv_med = df["Close"].rolling(self.period).median()[list_dt]
        mv_q1 = df["Close"].rolling(self.period).quantile(0.25)[list_dt]
        mv_q3 = df["Close"].rolling(self.period).quantile(0.75)[list_dt]
        mv_iqr = mv_q3 - mv_q1
        mv_lower = mv_q1 - mv_iqr * 1.5
        mv_upper = mv_q3 + mv_iqr * 1.5

        l1 = mpf.make_addplot(mv_upper, width=1.3, color='C1', linestyle='dotted', label='Upper bound', ax=ax)
        l2 = mpf.make_addplot(mv_q3, width=1, color='C2', linestyle='dashed', label='Q3 (75%)', ax=ax)
        l3 = mpf.make_addplot(mv_med, width=0.9, color='C3', label='Median', ax=ax)
        l4 = mpf.make_addplot(mv_q1, width=1, color='C4', linestyle='dashed', label='Q1 (25%)', ax=ax)
        l5 = mpf.make_addplot(mv_lower, width=1.3, color='C5', linestyle='dotted', label='Lower bound', ax=ax)
        apds.extend([l1, l2, l3, l4, l5])

    def save(self, filename):
        self.fig.savefig(filename)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
