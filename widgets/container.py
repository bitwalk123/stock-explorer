from PySide6.QtCharts import QChartView
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from structs.res import AppRes
from widgets.buttons import ToolButtonSave
from widgets.charts import PriceSeries, Chart, MarketTimeAxis, PriceAxis
from widgets.layout import VBoxLayout
from widgets.toolbar import ToolBar
from widgets.views import TickView


class WidgetTicker(QWidget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

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

    def setTimeRange(self, dt_start: QDateTime, dt_end: QDateTime):
        self.chart_view.setTimeRange(dt_start, dt_end)

    def setTitle(self, title: str):
        self.chart_view.setTitle(title)
