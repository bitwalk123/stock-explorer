import sys
import random
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, Qt, QDateTime
import pyqtgraph as pg
from pyqtgraph import DateAxisItem

class TrendChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイム風トレンドグラフ (PyQtGraph + PySide6)")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.plot_widget = pg.PlotWidget(axisItems={'bottom': DateAxisItem(orientation='bottom')})
        layout.addWidget(self.plot_widget)

        self.plot_widget.setTitle("リアルタイムトレンド")
        self.plot_widget.setLabel('left', "Y軸 (乱数)")

        self.start_time = time.time()
        self.end_time = self.start_time + 60

        self.plot_widget.setXRange(self.start_time, self.end_time)

        #self.plot_widget.setYRange(0, 100)

        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)

        self.line_plot = self.plot_widget.plot(pen=pg.mkPen(color=(70, 130, 180), width=2))
        self.scatter_plot = self.plot_widget.plot(
            symbol='o',
            symbolBrush=(255, 0, 0),
            symbolPen=(139, 0, 0),
            symbolSize=12,
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

        if current_time <= self.end_time:
            x_val = current_time
            y_val = random.randint(10, 90)

            self.x_data.append(x_val)
            self.y_data.append(y_val)

            self.line_plot.setData(self.x_data, self.y_data)
            self.scatter_plot.setData([x_val], [y_val])

            self.data_count += 1
            # ★★★ ここを修正しました ★★★
            # floatのx_val（UNIXタイムスタンプ）をintにキャストしてから渡す
            print(f"プロットデータ: 時刻={QDateTime.fromSecsSinceEpoch(int(x_val)).toString('%H:%M:%S')}, y={y_val}")
            # ★★★ ここまで修正 ★★★
        else:
            self.timer.stop()
            # ★★★ ここも修正しました ★★★
            # 同様に、floatのcurrent_timeをintにキャストしてから渡す
            print(f"開始時刻から60秒経過しました。タイマーを停止します。最終時刻: {QDateTime.fromSecsSinceEpoch(int(current_time)).toString('%H:%M:%S')}")
            # ★★★ ここまで修正 ★★★

if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    app = QApplication(sys.argv)
    window = TrendChartApp()
    window.show()
    sys.exit(app.exec())