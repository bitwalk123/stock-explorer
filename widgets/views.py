import math

from PySide6.QtCharts import QChartView
from PySide6.QtCore import QTime, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFileDialog

from funcs.tide import get_msec_delta_from_utc
from widgets.charts import (
    Chart,
    LastCloseSeries,
    MarketTimeAxis,
    PriceAxis,
    PriceSeries,
)


class TickView(QChartView):
    def __init__(self):
        super().__init__()
        # 最低サイズ
        self.setMinimumSize(1000, 300)

        # アンチエイリアスのレンダリング
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 市場開場時間と時差の定数
        self.msec_delta = get_msec_delta_from_utc()
        self.t_start = QTime(9, 0, 0)
        self.t_end = QTime(15, 30, 0)

        # プロットの開始フラグ
        self.plot_started = False

        # 前日終値用のフラグ
        self.lastclose_line = False

        # チャート
        self.chart = chart = Chart()
        self.setChart(chart)

        # ティックデータ用 Series
        self.series_tick = series_tick = PriceSeries()
        chart.addSeries(series_tick)

        # 前日終値用 Series
        self.series_lastclose = series_lastclose = LastCloseSeries()
        chart.addSeries(series_lastclose)

        # 市場時刻用の時間軸（横軸）
        self.ax_x = ax_x = MarketTimeAxis()
        chart.addAxis(ax_x, Qt.AlignmentFlag.AlignBottom)
        series_tick.attachAxis(ax_x)
        series_lastclose.attachAxis(ax_x)

        # 株価プロット用の数値軸（縦軸）
        self.ax_y = ax_y = PriceAxis()
        chart.addAxis(ax_y, Qt.AlignmentFlag.AlignLeft)
        series_tick.attachAxis(ax_y)
        series_lastclose.attachAxis(ax_y)

    def addLastCloseLine(self, y):
        x_min = self.t_start.msecsSinceStartOfDay() - self.msec_delta
        x_max = self.t_end.msecsSinceStartOfDay() - self.msec_delta
        self.series_lastclose.append(x_min, y)
        self.series_lastclose.append(x_max, y)
        self.adjustYrange(y)
        self.lastclose_line = True

    def appendPoint(self, x, y):
        self.series_tick.append(x, y)
        self.adjustYrange(y)

    def adjustYrange(self, y):
        if self.plot_started:
            y_min = self.ax_y.min()
            y_max = self.ax_y.max()
            if y < y_min:
                y_min = math.floor(y)
                self.ax_y.setRange(y_min, y_max)
            if y_max < y:
                y_max = math.ceil(y)
                self.ax_y.setRange(y_min, y_max)
        else:
            self.ax_y.setRange(
                math.floor(y - 0.5),
                math.ceil(y + 0.5)
            )
            self.plot_started = True

    def clearPoints(self):
        self.series_tick.clear()
        self.series_lastclose.clear()
        self.plot_started = False
        self.lastclose_line = False

    def lastClosePlotted(self) -> bool:
        return self.lastclose_line

    def saveChart(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Chart', '', 'PNG Files (*.png)'
        )
        if file_path:
            pixmap = self.grab()
            pixmap.save(file_path, 'png')
            print(f'プロットを {file_path} に保存しました。')

    def setTitle(self, title: str):
        self.chart.setTitle(title)
