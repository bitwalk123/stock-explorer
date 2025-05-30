import logging

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from modules.psar import RealtimePSAR
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

        # Parabolic SAR
        self.psar = RealtimePSAR()

        # PyQtGraph インスタンス
        self.chart = chart = TrendGraph()
        self.setCentralWidget(chart)

        # 株価トレンドライン
        self.trend_line: pg.PlotDataItem = chart.plot(pen=pg.mkPen(width=1))
        # self.trend_line.setDownsampling()
        # self.trend_line.setSkipFiniteCheck(True)

        # 最初のデータ点が追加されたか確認するフラグ
        self.trend_line_added = False

        # 最新株価
        self.point_latest: pg.PlotDataItem = chart.plot(symbol='o', symbolSize=5, pxMode=True)

        # 前日終値
        self.lastclose_line: pg.InfiniteLine | None = None

        # 上昇トレンド
        self.trend_bull: pg.PlotDataItem = chart.plot(
            pen=None,
            symbol='o',
            symbolPen=(255, 0, 255),
            symbolSize=2,
            pxMode=True,
        )
        self.trend_bull.setDownsampling()
        self.trend_bull.setSkipFiniteCheck(True)
        self.trend_bull_added = False

        # 下降トレンド
        self.trend_bear: pg.PlotDataItem = chart.plot(
            pen=None,
            symbol='o',
            symbolPen=(0, 139, 139),
            symbolSize=2,
            pxMode=True,
        )
        self.trend_bear.setDownsampling()
        self.trend_bear.setSkipFiniteCheck(True)
        self.trend_bear_added = False

        self.dock = dock = DockTrader(res)
        # dock.saveClicked.connect(trend_graph.saveChart)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def addLastCloseLine(self, value: float):
        self.lastclose_line = pg.InfiniteLine(
            pos=value,
            angle=0,
            pen=pg.mkPen(color=(255, 0, 0), width=1)
        )
        self.chart.addItem(self.lastclose_line)

    def appendData(self, x, y):
        if self.trend_line_added:
            arr_x = np.append(self.trend_line.xData, x)
            arr_y = np.append(self.trend_line.yData, y)
        else:
            arr_x = [x]
            arr_y = [y]
            self.trend_line_added = True
        self.trend_line.setData(arr_x, arr_y)

        self.point_latest.setData([x], [y])

        # Parabolic SAR
        ret = self.psar.add(y)
        y_psar = ret.psar
        if 0 < ret.trend:
            if self.trend_bull_added:
                arr_bull_x = np.append(self.trend_bull.xData, x)
                arr_bull_y = np.append(self.trend_bull.yData, y_psar)
            else:
                arr_bull_x = [x]
                arr_bull_y = [y_psar]
                self.trend_bull_added = True
            self.trend_bull.setData(arr_bull_x, arr_bull_y)
        elif ret.trend < 0:
            if self.trend_bear_added:
                arr_bear_x = np.append(self.trend_bear.xData, x)
                arr_bear_y = np.append(self.trend_bear.yData, y_psar)
            else:
                arr_bear_x = [x]
                arr_bear_y = [y_psar]
                self.trend_bear_added = True
            self.trend_bear.setData(arr_bear_x, arr_bear_y)

        self.dock.setPrice(y)

    def clear(self):
        pass
        # self.trend_graph.clear()

    def getDataSize(self) -> int:
        return len(self.trend_line.xData)

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
        self.chart.setXRange(ts_start, ts_end)

    def setTitle(self, title: str):
        self.chart.setTitle(title)

    def setSheetName(self, name_sheet: str):
        self.name_sheet = name_sheet


class TraderUnitDebug(TraderUnit):
    def __init__(self, row: int, res: AppRes):
        super().__init__(row, res)
