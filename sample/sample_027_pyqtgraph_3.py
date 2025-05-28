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
        self.setWindowTitle("リアルタイム風トレンドグラフ (PyQtGraph + PySide6)")
        self.setFixedSize(800, 600)

        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout(base)

        # DateAxisItem を使用 (変更なし)
        self.chart = chart = pg.PlotWidget(
            axisItems={'bottom': DateAxisItem(orientation='bottom')}
        )
        layout.addWidget(chart)

        self.start_time = time.time()  # time.time() は既にミリ秒精度を含むfloat
        self.end_time = self.start_time + 60  # 60秒後
        self.chart.setXRange(self.start_time, self.end_time)

        self.chart.showGrid(x=True, y=True, alpha=0.5)

        self.trend_line = self.chart.plot(pen=pg.mkPen(color=(0, 0, 0), width=1))
        self.point_latest = self.chart.plot(
            symbol='o',
            symbolBrush=(255, 0, 0),
            symbolPen=(128, 0, 0),
            symbolSize=10,
            pxMode=True
        )

        self.x_data = []  # 秒単位のUNIXタイムスタンプ (float) を格納
        self.y_data = []
        self.data_count = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)

    def update_chart(self):
        # time.time() はマイクロ秒精度まで提供されるため、これをX軸の値として使用
        current_time = time.time()

        # コンソール出力用の整形
        dt_object = datetime.datetime.fromtimestamp(current_time)
        formatted_time = dt_object.strftime("%H:%M:%S.%f")

        if current_time <= self.end_time:
            x_val = current_time  # プロットデータはfloatのまま
            y_val = random.randint(0, 100)

            self.x_data.append(x_val)
            self.y_data.append(y_val)

            self.trend_line.setData(self.x_data, self.y_data)
            self.point_latest.setData([x_val], [y_val])

            self.data_count += 1

            print(f"プロットデータ: 時刻={formatted_time}, y={y_val}")
        else:
            self.timer.stop()
            print(f"開始時刻から60秒経過しました。タイマーを停止します。最終時刻: {formatted_time}")

            # データ抽出部分は変更なし。xデータはfloatのタイムスタンプとして得られる
            print("\n--- データ抽出開始 ---")
            extracted_x, extracted_y = self.trend_line.getData()

            print(f"抽出されたXデータ点の数: {len(extracted_x)}")
            print(f"抽出されたYデータ点の数: {len(extracted_y)}")

            # 例として、最初の5点と最後の5点を出力 (ここもミリ秒表示に)
            print("最初の5点:")
            for i in range(min(5, len(extracted_x))):
                print(f"  X: {extracted_x[i]}, Y: {extracted_y[i]}")

            print("最後の5点:")
            for i in range(max(0, len(extracted_x) - 5), len(extracted_x)):
                print(f"  X: {extracted_x[i]}, Y: {extracted_y[i]}")
            print("--- データ抽出終了 ---")


if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec())
