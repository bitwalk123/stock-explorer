import logging

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from structs.res import AppRes
from widgets.buttons import ToolButtonSave
from widgets.layout import VBoxLayout
from widgets.toolbar import ToolBar
from widgets.views import TickView


class TraderUnit(QWidget):
    def __init__(self, row: int, res: AppRes):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.res = res
        self.row = row

        self.chart_view = chart_view = TickView(res)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        toolbar = ToolBar()
        but_save = ToolButtonSave(res)
        but_save.clicked.connect(chart_view.saveChart)
        toolbar.addWidget(but_save)

        layout = VBoxLayout()
        self.setLayout(layout)

        layout.addWidget(toolbar)
        layout.addWidget(chart_view)

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
