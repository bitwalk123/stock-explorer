import sys
import random
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter

class RealTimeChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.series = QLineSeries()
        self.series.setName("リアルタイムデータ")

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().setVisible(True)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # X軸
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 100)
        self.axis_x.setTitleText("X軸")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Y軸
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Y軸")
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)

        # 固定ライン (y=60)
        self.fixed_line = QLineSeries()
        for x in range(101):
            self.fixed_line.append(x, 60)
        self.chart.addSeries(self.fixed_line)
        self.fixed_line.attachAxis(self.axis_x)
        self.fixed_line.attachAxis(self.axis_y)
        self.fixed_line.setColor(Qt.GlobalColor.red)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setCentralWidget(self.chart_view)
        self.setWindowTitle("リアルタイム トレンドチャート")
        self.resize(800, 600)

        self.data_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)

    def update_chart(self):
        if self.data_count >= 100:
            self.timer.stop()
            return

        start_time = time.time()
        x = self.data_count
        y = random.randint(0, 100)
        self.series.append(x, y)

        # Y軸のスケール更新 (pointsVector() -> points() に修正)
        min_y, max_y = min(p.y() for p in self.series.points()), max(p.y() for p in self.series.points())
        self.axis_y.setRange(min_y - (min_y % 10), max_y + (10 - max_y % 10))

        elapsed_time = (time.time() - start_time) * 1000
        print(f"処理時間: {elapsed_time:.3f} ms")

        self.data_count += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeChart()
    window.show()
    sys.exit(app.exec())
