import math

from PySide6.QtCharts import QChartView, QValueAxis, QLineSeries, QChart
from PySide6.QtCore import QTime, Qt, QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFileDialog

from funcs.tide import get_msec_delta_from_utc
from structs.res import AppRes
from widgets.charts import (
    Chart,
    LastCloseSeries,
    MarketTimeAxis,
    PriceAxis,
    PriceSeries,
)


class TickViewOld(QChartView):
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
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
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

    def adjust_value_axis_ticks(self, axis: QValueAxis, series: QLineSeries):
        """
        Gemini にお知れてもらった軸のスケール調整の方法
        少し無駄のある事、前日終値の横線の対応が必要なのでしばらく保留
        """
        points = series.points()
        if not points:
            return

        min_val = min(point.y() for point in points)
        max_val = max(point.y() for point in points)

        # キリの良い刻み幅を計算する
        range_val = max_val - min_val
        if range_val == 0:
            step = 1
        else:
            # 大まかな刻み幅を計算
            rough_step = range_val / 5.0  # 例えば5分割
            # 1, 2, 5, 10, 20, 50, ... のようなキリの良い数値に調整
            power = 10 ** math.floor(math.log10(rough_step))
            normalized_step = rough_step / power
            if normalized_step < 2:
                step = 1 * power
            elif normalized_step < 5:
                step = 2 * power
            else:
                step = 5 * power

        # 最小値と最大値をキリの良い数値に調整
        nice_min = math.floor(min_val / step) * step
        nice_max = math.ceil(max_val / step) * step

        axis.setTickInterval(step)
        axis.setRange(nice_min, nice_max)

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


class TickView(QChartView):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.dt_start: None | QDateTime = None
        self.dt_end: None | QDateTime = None

        # ティックデータ用 Series
        self.series_tick = series_tick = PriceSeries()

        # 前日終値用 Series
        self.series_lastclose = series_lastclose = LastCloseSeries()

        # X軸（市場時間）
        self.axis_x = axis_x = MarketTimeAxis()
        series_tick.attachAxis(axis_x)
        series_lastclose.attachAxis(axis_x)

        # Y軸（株価）
        axis_y = PriceAxis()
        series_tick.attachAxis(axis_y)
        series_lastclose.attachAxis(axis_y)

        self.chart = chart = Chart()
        chart.setMinimumSize(1000, 300)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        chart.addSeries(series_tick)
        chart.addSeries(series_lastclose)
        self.setChart(chart)

    def addLastCloseLine(self, y):
        pass

    def saveChart(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Chart', '', 'PNG Files (*.png)'
        )
        if file_path:
            pixmap = self.grab()
            pixmap.save(file_path, 'png')
            print(f'プロットを {file_path} に保存しました。')

    def setTimeRange(self, dt_start: QDateTime, dt_end: QDateTime):
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.axis_x.setRange(dt_start, dt_end)

    def setTitle(self, title: str):
        self.chart.setTitle(title)
