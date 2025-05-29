import logging

import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from widgets.docks import DockTrader
from widgets.graph import TrendGraph


class TraderUnit(QMainWindow):
    def __init__(self, row: int, res: AppRes):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.ticker_code = ""
        self.name_sheet = ""
        self.res = res
        self.row = row

        self.x_data = []  # 秒単位のUNIXタイムスタンプ (float) を格納
        self.y_data = []

        # PyQtGraph インスタンス
        self.trend_graph = trend_graph = TrendGraph()
        self.setCentralWidget(trend_graph)

        # 株価トレンドライン
        self.trend_line = trend_graph.plot(pen=pg.mkPen(width=1))
        # 最新株価
        self.point_latest = trend_graph.plot(symbol='o', symbolSize=5, pxMode=True)

        self.dock = dock = DockTrader(res)
        # dock.saveClicked.connect(trend_graph.saveChart)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def clear(self):
        pass
        # self.trend_graph.clear()

    def getRow(self) -> int:
        return self.row

    def getSheetName(self) -> str:
        return self.name_sheet

    def getTickerCode(self) -> str:
        return self.ticker_code

    def setRow(self, row: int):
        self.row = row

    def setTickerCode(self, ticker_code: str):
        self.ticker_code = ticker_code

    def setTimeRange(self, ts_start, ts_end):
        self.trend_graph.setXRange(ts_start, ts_end)

    def setSheetName(self, name_sheet: str):
        self.name_sheet = name_sheet

    def updateTrend(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

        self.trend_line.setData(self.x_data, self.y_data)
        self.point_latest.setData([x], [y])

    def updateTrendLine(self, df: pd.DataFrame):
        self.x_data = df['Time']
        self.y_data = df['Price']

        self.trend_line.setData(self.x_data, self.y_data)


class TraderUnitDebug(TraderUnit):
    def __init__(self, row: int, res: AppRes):
        super().__init__(row, res)
