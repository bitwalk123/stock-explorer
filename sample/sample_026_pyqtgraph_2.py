import datetime
import sys
import random
import time
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QTimer
import pyqtgraph as pg
from pyqtgraph import DateAxisItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイム風トレンドグラフ (PySide6 + PyQtGraph)")
        self.setFixedSize(600, 400)

        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout(base)

        self.chart = chart = pg.PlotWidget(
            axisItems={'bottom': DateAxisItem(orientation='bottom')}
        )
        layout.addWidget(chart)

        self.start_time = time.time()
        self.end_time = self.start_time + 60
        self.chart.setXRange(self.start_time, self.end_time)

        self.chart.showGrid(x=True, y=True, alpha=0.5)

        self.trend_line = self.chart.plot(pen=pg.mkPen(color=(0, 0, 0), width=1))
        self.scatter_plot = self.chart.plot(
            symbol='o',
            symbolBrush=(255, 0, 0),
            symbolPen=(128, 0, 0),
            symbolSize=10,
            pxMode=True
        )

        self.x_data = []
        self.y_data = []
        self.data_count = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)

    def update_chart(self):
        current_time = time.time()
        dt_object = datetime.datetime.fromtimestamp(current_time)
        formatted_time = dt_object.strftime("%H:%M:%S")

        if current_time <= self.end_time:
            x_val = current_time
            y_val = random.randint(0, 100)

            self.x_data.append(x_val)
            self.y_data.append(y_val)

            self.trend_line.setData(self.x_data, self.y_data)
            self.scatter_plot.setData([x_val], [y_val])

            self.data_count += 1

            print(f"プロットデータ: 時刻={formatted_time}, y={y_val}")
        else:
            self.timer.stop()
            print(f"開始時刻から60秒経過しました。タイマーを停止します。最終時刻: {formatted_time}")


if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec())
