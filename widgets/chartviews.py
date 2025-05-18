from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QTime, Qt
from PySide6.QtGui import QPainter, QPen


def get_pen() -> QPen:
    pen = QPen(Qt.GlobalColor.darkGray)
    pen.setWidthF(0.5)
    return pen


class TradeView(QChartView):
    def __init__(self):
        super().__init__()

        # view = QChartView(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.series = series = QLineSeries()
        series.setPen(get_pen())
        series.setPointsVisible(True)
        series.setMarkerSize(0.75)

        self.axis_x = axis_x = QDateTimeAxis()
        axis_x.setTickCount(14)
        axis_x.setFormat('HH:mm')

        axis_x_min = axis_x.min()
        axis_x_min.setTime(QTime.fromString('9:00:00', 'H:mm:ss'))
        axis_x_max = axis_x.max()
        axis_x_max.setTime(QTime.fromString('15:30:00', 'H:mm:ss'))
        axis_x.setRange(axis_x_min, axis_x_max)

        self.axis_y = axis_y = QValueAxis()
        axis_y.setRange(0, 1)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        self.setChart(chart)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
