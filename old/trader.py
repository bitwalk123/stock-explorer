import logging

import numpy as np
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from widgets.docks import DockTrader
from widgets.views import ChartView


class TraderUnit(QMainWindow):
    def __init__(self, row: int, res: AppRes):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.ticker_code = ""
        self.name_sheet = ""
        self.res = res
        self.row = row

        self.chart_view = chart_view = ChartView(res)
        self.setCentralWidget(chart_view)

        self.dock = dock = DockTrader(res)
        dock.saveClicked.connect(chart_view.saveChart)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def addLastCloseLine(self, y: float):
        self.chart_view.addLastCloseLine(y)

    def appendPoint(self, dt: QDateTime, y: float):
        self.chart_view.appendPoint(dt, y)
        self.dock.setPrice(y)

    def appendPointTimestamp(self, x: int, y: float):
        self.chart_view.appendPointTimestamp(x, y)
        self.dock.setPrice(y)

    def appendPoints(self, array_x: np.array, array_y: np.array):
        self.chart_view.appendPoints(array_x, array_y)

    def clear(self):
        self.chart_view.clear()

    def getDataSet(self):
        return self.chart_view.getDataSet()

    def getRow(self) -> int:
        return self.row

    def getTickerCode(self) -> str:
        return self.ticker_code

    def setRow(self, row: int):
        self.row = row

    def setTickerCode(self, ticker_code: str):
        self.ticker_code = ticker_code

    def setTimeRange(self, dt_start: QDateTime, dt_end: QDateTime):
        self.chart_view.setTimeRange(dt_start, dt_end)

    def getSheetName(self) -> str:
        return self.name_sheet

    def setSheetName(self, name_sheet: str):
        self.name_sheet = name_sheet

    def setTitle(self, title: str):
        self.chart_view.setTitle(title)


class TraderUnitDebug(TraderUnit):
    def __init__(self, row: int, res: AppRes):
        super().__init__(row, res)
