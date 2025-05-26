import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QPainter
from random import randint
import math


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 500)

        chart = QChart()
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        series = QLineSeries()

        # ダミーデータの生成
        now = QDateTime.currentDateTime()
        for i in range(20):
            timestamp = now.addSecs(i * 3600)
            value = randint(10, 100)
            series.append(timestamp.toMSecsSinceEpoch(), value)

        chart.addSeries(series)

        # 横軸の設定 (QDateTimeAxis)
        datetime_axis = QDateTimeAxis()
        datetime_axis.setFormat("yyyy/MM/dd hh:mm:ss")
        datetime_axis.setTitleText("時間")
        chart.addAxis(datetime_axis, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(datetime_axis)

        # 縦軸の設定 (QValueAxis)
        value_axis = QValueAxis()
        value_axis.setTitleText("値")
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(value_axis)

        # 縦軸のtickをキリの良い数値にする
        self.adjust_value_axis_ticks(value_axis, series)

        self.setCentralWidget(chart_view)
        self.setWindowTitle("トレンドチャート")

    def adjust_value_axis_ticks(self, axis: QValueAxis, series: QLineSeries):
        points = series.points()
        if not points:
            return

        min_val = min(point.y() for point in points)
        max_val = max(point.y() for point in points)

        # キリの良い刻み幅を計算する
        range_val = max_val - min_val
        if range_val == 0:
            step = 1
        else:
            # 大まかな刻み幅を計算
            rough_step = range_val / 5.0  # 例えば5分割
            # 1, 2, 5, 10, 20, 50, ... のようなキリの良い数値に調整
            power = 10 ** math.floor(math.log10(rough_step))
            normalized_step = rough_step / power
            if normalized_step < 2:
                step = 1 * power
            elif normalized_step < 5:
                step = 2 * power
            else:
                step = 5 * power

        # 最小値と最大値をキリの良い数値に調整
        nice_min = math.floor(min_val / step) * step
        nice_max = math.ceil(max_val / step) * step

        axis.setTickInterval(step)
        axis.setRange(nice_min, nice_max)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
