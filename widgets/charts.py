import datetime
import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import yfinance as yf
from PySide6.QtCharts import QChart, QLineSeries, QDateTimeAxis, QValueAxis, QScatterSeries
from PySide6.QtCore import QMargins, QTime, Qt
from PySide6.QtGui import QPen, QColor

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from funcs.common import get_font_monospace
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

        # 過去 1 年分のデータの分離用
        # self.tdelta_1y = datetime.timedelta(days=366)
        # 過去 約 9ヶ月分のデータの分離用
        self.tdelta_1y = datetime.timedelta(days=280)
        # for Bollinger bands
        self.period = 20

        # yfinance.Ticker インスタンス
        self.ticker: yf.Ticker | None = None

        # データフレーム
        self.df_long = pd.DataFrame()
        self.df = pd.DataFrame()

        font = os.path.join(res.dir_font, "RictyDiminished-Regular.ttf")
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams["font.family"] = font_prop.get_name()
        plt.rcParams["font.size"] = 14

        self.ax = dict()
        n = 2

        if n > 1:
            gs = self.fig.add_gridspec(
                n, 1,
                wspace=0.0, hspace=0.0,
                height_ratios=[3 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex="col")):
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
        self.ticker = ticker
        try:
            # 日足で過去データを取得
            self.df_long: pd.DataFrame = self.ticker.history(period="5y", interval="1d")
        except Exception as e:
            list_msg = list()
            for msg in e.args:
                list_msg.append(msg)
            # エラー・ダイアログ
            dlg = DialogError('\n'.join(list_msg))
            dlg.exec()
            return

        # ローソク足のチャートには、そのうち過去 1 年分のみ使用する
        dt_last = self.df_long.index[len(self.df_long) - 1]
        self.df = self.df_long[dt_last - self.tdelta_1y <= self.df_long.index]

        # プロット
        self.plot_main()

    def plot_add_robust_bollinger(self, ax: plt.Axes, list_plot: list):
        """
        Robust Bollinger bands
        :param ax:
        :param list_plot:
        :return:
        """
        list_dt = self.df.index
        ser_close = self.df_long["Close"]

        # 移動メジアン等を算出
        mv_med = ser_close.rolling(self.period).median()[list_dt]
        mv_q1 = ser_close.rolling(self.period).quantile(0.25)[list_dt]
        mv_q3 = ser_close.rolling(self.period).quantile(0.75)[list_dt]
        mv_iqr = mv_q3 - mv_q1
        mv_lower = mv_q1 - mv_iqr * 1.5
        mv_upper = mv_q3 + mv_iqr * 1.5

        l1 = mpf.make_addplot(mv_upper, width=1.3, color="C3", linestyle="dotted", label="Upper bound", ax=ax)
        l2 = mpf.make_addplot(mv_q3, width=1, color="C2", linestyle="dashed", label="Q3 (75%)", ax=ax)
        l3 = mpf.make_addplot(mv_med, width=0.9, color="C0", label="Median", ax=ax)
        l4 = mpf.make_addplot(mv_q1, width=1, color="C2", linestyle="dashed", label="Q1 (25%)", ax=ax)
        l5 = mpf.make_addplot(mv_lower, width=1.3, color="C3", linestyle="dotted", label="Lower bound", ax=ax)
        list_plot.extend([l1, l2, l3, l4, l5])

    def plot_main(self):
        """
        プロット（メイン）
        :return:
        """
        list_plot = list()
        # Robust Bollinger bands
        self.plot_add_robust_bollinger(self.ax[0], list_plot)

        # 消去
        clear_axes(self.fig)

        # ローソク足
        mpf.plot(
            self.df,
            type="candle",
            style="default",
            addplot=list_plot,
            datetime_format="%y-%m-%d",
            xrotation=0,
            ax=self.ax[0],
            volume=self.ax[1],
        )

        # テクニカル指標の追加によって、下限がマイナスになってしまう場合があるため
        y_lower, y_upper = self.ax[0].get_ylim()
        if y_lower < 0:
            self.ax[0].set_ylim(0, y_upper)

        # グリッド線
        draw_grid(self.fig)

        # 凡例
        self.ax[0].legend(loc="best", fontsize=8)

        # チャート・タイトル
        title = get_chart_title(self.ticker)
        self.ax[0].set_title(title)

        # 再描画
        refresh_draw(self.fig)

    def save(self, filename):
        self.fig.savefig(filename)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)


class Chart(QChart):
    def __init__(self):
        super().__init__()
        self.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.setMargins(QMargins(0, 0, 0, 0))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setBackgroundRoundness(0)
        # self.setTitleFont(get_font_monospace())
        self.legend().hide()


class PriceSeries(QLineSeries):
    def __init__(self):
        super().__init__()
        self.setPointsVisible(True)
        pen = QPen(QColor(Qt.GlobalColor.darkGray))
        pen.setWidthF(0.5)
        self.setPen(pen)
        self.setMarkerSize(0.75)


class LastCloseSeries(QLineSeries):
    def __init__(self):
        super().__init__()
        self.setPointsVisible(False)
        pen = QPen(QColor(Qt.GlobalColor.red))
        pen.setWidthF(0.5)
        self.setPen(pen)


class PSARSeries(QScatterSeries):
    def __init__(self):
        super().__init__()
        # Parabolic SAR Series
        self.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)  # 円形
        self.setMarkerSize(5)  # 点のサイズ
        self.setPen(QPen(Qt.PenStyle.NoPen))


class PSARBullSeries(PSARSeries):
    def __init__(self):
        super().__init__()
        # Parabolic SAR Series （上昇トレンド用: 赤点）
        self.setName("Up trend")
        self.setColor(QColor(Qt.GlobalColor.red))  # 赤色


class PSARBearSeries(PSARSeries):
    def __init__(self):
        super().__init__()
        # Parabolic SAR Series （下降トレンド用: 青点）
        self.setName("Down trend")
        self.setColor(QColor(Qt.GlobalColor.blue))  # 青色


class MarketTimeAxis(QDateTimeAxis):
    def __init__(self):
        super().__init__()
        self.setLabelsFont(get_font_monospace())
        self.setTickCount(14)
        self.setFormat("HH:mm")

        ax_x_min = self.min()
        ax_x_min.setTime(QTime.fromString("9:00:00", "H:mm:ss"))
        ax_x_max = self.max()
        ax_x_max.setTime(QTime.fromString("15:30:00", "H:mm:ss"))
        self.setRange(ax_x_min, ax_x_max)


class PriceAxis(QValueAxis):
    def __init__(self):
        super().__init__()
        self.setLabelsFont(get_font_monospace())
