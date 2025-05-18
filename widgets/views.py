from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QTime, Qt
from PySide6.QtGui import QPainter, QPen


class TickView(QChartView):
    def __init__(self):
        super().__init__()
        self.plot_started = False
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.series = series = QLineSeries()
        series.setPen(self.getPen())
        series.setPointsVisible(True)
        series.setMarkerSize(0.75)

        self.ax_x = ax_x = QDateTimeAxis()
        ax_x.setTickCount(14)
        ax_x.setFormat('HH:mm')

        ax_x_min = ax_x.min()
        ax_x_min.setTime(QTime.fromString('9:00:00', 'H:mm:ss'))
        ax_x_max = ax_x.max()
        ax_x_max.setTime(QTime.fromString('15:30:00', 'H:mm:ss'))
        ax_x.setRange(ax_x_min, ax_x_max)

        self.ax_y = ax_y = QValueAxis()
        ax_y.setRange(0, 1)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        self.setChart(chart)

        chart.addAxis(ax_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(ax_x)

        chart.addAxis(ax_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(ax_y)

    def appendPoint(self, x, y):
        self.series.append(x, y)
        self.adjustYrange(y)

    def adjustYrange(self, y):
        if self.plot_started:
            y_min = self.ax_y.min()
            y_max = self.ax_y.max()
            if y < y_min:
                y_min = y
                self.ax_y.setRange(y_min, y_max)
            if y_max < y:
                y_max = y
                self.ax_y.setRange(y_min, y_max)
        else:
            self.ax_y.setRange(y - 0.5, y + 0.5)
            self.plot_started = True

    @staticmethod
    def getPen() -> QPen:
        pen = QPen(Qt.GlobalColor.darkGray)
        pen.setWidthF(0.5)
        return pen
