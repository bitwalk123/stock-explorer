import logging
import math
import os

import numpy as np
import pandas as pd
from PySide6.QtCharts import (
    QChartView,
)
from PySide6.QtCore import (
    QDateTime,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFileDialog

from structs.res import AppRes
from widgets.charts import (
    Chart,
    LastCloseSeries,
    MarketTimeAxis,
    PriceAxis,
    PriceSeries, PSARBearSeries, PSARBullSeries,
)


class ChartView(QChartView):
    def __init__(self, res: AppRes):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.res = res
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.title: None | str = None
        self.dt_start: None | QDateTime = None
        self.dt_end: None | QDateTime = None

        self.chart = chart = Chart()
        chart.setMinimumSize(1000, 200)
        self.setChart(chart)

        # ティックデータ用 Series
        self.series_tick = series_tick = PriceSeries()
        chart.addSeries(series_tick)

        # 前日終値用 Series
        self.series_lastclose = series_lastclose = LastCloseSeries()
        chart.addSeries(series_lastclose)

        # Parabolic SAR Series（上昇トレンド用: 赤の点）
        self.series_bull = series_bull = PSARBullSeries()
        chart.addSeries(series_bull)

        # Parabolic SAR Series（下降トレンド用: 青の点）
        self.series_bear = series_bear = PSARBearSeries()
        chart.addSeries(series_bear)

        # X軸（市場時間）
        self.axis_x = axis_x = MarketTimeAxis()
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series_tick.attachAxis(axis_x)
        series_lastclose.attachAxis(axis_x)
        series_bull.attachAxis(axis_x)
        series_bear.attachAxis(axis_x)

        # Y軸（株価）
        self.axis_y = axis_y = PriceAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series_tick.attachAxis(axis_y)
        series_lastclose.attachAxis(axis_y)
        series_bull.attachAxis(axis_y)
        series_bear.attachAxis(axis_y)

    def appendPoint(self, dt: QDateTime, y: float):
        self.series_tick.append(dt.toMSecsSinceEpoch(), y)
        self.update_y_axis(y)

    def appendPointTimestamp(self, x: int, y: float):
        self.series_tick.append(x, y)
        self.update_y_axis(y)

    def appendPoints(self, array_x: np.array, array_y: np.array):
        self.series_tick.appendNp(array_x, array_y)
        y_min = np.min(array_y)
        y_max = np.max(array_y)
        self.axis_y.setRange(y_min, y_max)

    def addLastCloseLine(self, y: float):
        self.series_lastclose.append(self.dt_start.toMSecsSinceEpoch(), y)
        self.series_lastclose.append(self.dt_end.toMSecsSinceEpoch(), y)
        self.update_y_axis(y)

    def clear(self):
        self.series_tick.clear()
        self.series_lastclose.clear()
        self.axis_y.setRange(0, 1)

    def getDateYMD(self) -> str:
        try:
            qdate = self.dt_start.date()
            return f"{qdate.year():04}{qdate.month():02}{qdate.day():02}"
        except AttributeError as e:
            self.logger.error(e)
            return "00000000"

    def getDataSet(self) -> pd.DataFrame:
        list_x = list()
        list_y = list()

        for point in self.series_tick.points():
            list_x.append(point.x())
            list_y.append(point.y())

        return pd.DataFrame({"Time": list_x, "Price": list_y})

    def getTitle(self) -> str:
        return self.title

    def saveChart(self):
        date = self.getDateYMD()
        ticker = self.getTitle()
        filename = f"{date}_{ticker}.png"
        default_path = os.path.join(self.res.dir_output, filename)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Chart",
            default_path,
            "PNG Files (*.png)"
        )

        if file_path:
            # 拡張子 .png が含まれているかチェック
            if not file_path.lower().endswith(".png"):
                file_path += ".png"

            pixmap = self.grab()
            pixmap.save(file_path, "png")
            self.logger.info(f"プロットを {file_path} に保存しました。")

    def setTimeRange(self, dt_start: QDateTime, dt_end: QDateTime):
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.axis_x.setRange(dt_start, dt_end)

    def setTitle(self, title: str):
        self.title = title
        self.chart.setTitle(title)

    def update_y_axis(self, y: float):
        y_min = self.axis_y.min()
        y_max = self.axis_y.max()

        if y_min == 0 and y_max == 1:
            y_min = y - 1
            y_max = y + 1
        elif y < y_min:
            y_min = math.floor(y - 1)
        elif y_max < y:
            y_max = math.ceil(y + 1)
        else:
            return

        self.axis_y.setRange(y_min, y_max)
