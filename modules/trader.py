import logging

from PySide6.QtCore import QDateTime, QMargins
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QMainWindow

from structs.res import AppRes
from widgets.buttons import ToolButtonSave
from widgets.layout import VBoxLayout
from widgets.toolbar import ToolBar, ToolBarTrader
from widgets.views import TickView


class TraderUnit(QMainWindow):
    def __init__(self, row: int, res: AppRes):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.res = res
        self.row = row

        self.chart_view = chart_view = TickView(res)
        self.setCentralWidget(chart_view)

        toolbar = ToolBarTrader(res)
        toolbar.saveClicked.connect(chart_view.saveChart)
        self.addToolBar(toolbar)

    def addLastCloseLine(self, y: float):
        self.chart_view.addLastCloseLine(y)

    def appendPoint(self, dt: QDateTime, y: float):
        self.chart_view.appendPoint(dt, y)

    def getRow(self) -> int:
        return self.row

    def setRow(self, row: int):
        self.row = row

    def setTimeRange(self, dt_start: QDateTime, dt_end: QDateTime):
        self.chart_view.setTimeRange(dt_start, dt_end)

    def setTitle(self, title: str):
        self.chart_view.setTitle(title)


class TraderUnitDebug(TraderUnit):
    def __init__(self, row: int, res: AppRes):
        super().__init__(row, res)
