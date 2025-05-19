from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QTime, Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)


class TickView(QChartView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.msec_delta = 9 * 60 * 60 * 1000
        self.t_start = QTime(9, 0, 0)
        self.t_end = QTime(15, 30, 0)

        self.plot_started = False
        self.lastclose_line = False

        chart = QChart()
        chart.legend().hide()
        self.setChart(chart)

        self.series_tick = series_tick = QLineSeries()
        series_tick.setPointsVisible(True)
        series_tick.setPen(self.getPenTick())
        series_tick.setMarkerSize(0.75)
        chart.addSeries(series_tick)

        self.series_lastclose = series_lastclose = QLineSeries()
        series_lastclose.setPointsVisible(False)
        series_lastclose.setPen(self.getPenLastClose())
        chart.addSeries(series_lastclose)

        self.ax_x = ax_x = QDateTimeAxis()
        ax_x.setTickCount(14)
        ax_x.setFormat('HH:mm')

        self.ax_x_min = ax_x_min = ax_x.min()
        ax_x_min.setTime(QTime.fromString('9:00:00', 'H:mm:ss'))
        self.ax_x_max = ax_x_max = ax_x.max()
        ax_x_max.setTime(QTime.fromString('15:30:00', 'H:mm:ss'))
        ax_x.setRange(ax_x_min, ax_x_max)

        chart.addAxis(ax_x, Qt.AlignmentFlag.AlignBottom)
        series_tick.attachAxis(ax_x)
        series_lastclose.attachAxis(ax_x)

        self.ax_y = ax_y = QValueAxis()
        ax_y.setRange(0, 1)

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
                y_min = y
                self.ax_y.setRange(y_min, y_max)
            if y_max < y:
                y_max = y
                self.ax_y.setRange(y_min, y_max)
        else:
            self.ax_y.setRange(y - 0.5, y + 0.5)
            self.plot_started = True

    def clearPoints(self):
        self.series_tick.clear()
        self.series_lastclose.clear()
        self.plot_started = False
        self.lastclose_line = False

    @staticmethod
    def getPenTick() -> QPen:
        color = QColor(64, 64, 64)
        pen = QPen(color)
        pen.setWidthF(1)
        return pen

    @staticmethod
    def getPenLastClose() -> QPen:
        color = QColor(255, 0, 0)
        pen = QPen(color)
        pen.setWidthF(0.5)
        return pen

    def lastClosePlotted(self) -> bool:
        return self.lastclose_line
