import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

class TrendChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QChart トレンドチャート")
        self.setGeometry(100, 100, 800, 600)

        self.data_count = 0
        self.max_data_points = 100
        self.current_y_values = [] # 動的なY軸スケール調整のために現在のY値を保持

        self.chart = QChart()
        self.chart.setTitle("ランダムデータトレンド")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # データ系列の準備
        self.series = QLineSeries()
        self.series.setName("データ")
        self.chart.addSeries(self.series)

        # 固定の横線（y=60）の準備
        self.horizontal_line_series = QLineSeries()
        self.horizontal_line_series.setName("目標ライン (y=60)")
        self.horizontal_line_series.setColor(QColor(255, 0, 0)) # 赤色
        # x軸の全範囲にわたって線を引く
        self.horizontal_line_series.append(0, 60)
        self.horizontal_line_series.append(100, 60)
        self.chart.addSeries(self.horizontal_line_series)

        # X軸の設定 (0から100で固定)
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 100)
        self.axis_x.setTickCount(11) # 0, 10, ..., 100 の11個のティック
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setTitleText("X軸")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom) # X軸をチャートに追加

        # Y軸の設定 (動的に変更、10刻み)
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Y軸")
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft) # Y軸をチャートに追加

        # ★★★ ここから変更点 ★★★
        # 各系列に軸をアタッチする
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        self.horizontal_line_series.attachAxis(self.axis_x)
        self.horizontal_line_series.attachAxis(self.axis_y)
        # ★★★ ここまで変更点 ★★★

        self.update_y_axis_range() # 初期Y軸の範囲を設定

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.chart_view)
        self.setCentralWidget(central_widget)

        # QTimer の設定
        self.timer = QTimer(self)
        self.timer.setInterval(1000) # 1秒ごと
        self.timer.timeout.connect(self.add_data_point)
        self.timer.start()

    def add_data_point(self):
        if self.data_count >= self.max_data_points:
            self.timer.stop()
            print("データ追加が完了しました。")
            return

        x = self.data_count
        y = random.randint(0, 100) # 0から100までのランダムな値

        self.series.append(x, y)
        self.current_y_values.append(y)
        self.data_count += 1

        self.update_y_axis_range() # データ追加ごとにY軸の範囲を更新

    def update_y_axis_range(self):
        if not self.current_y_values:
            # 初期状態またはデータがない場合、デフォルトの範囲を設定
            min_y = 0
            max_y = 100
        else:
            min_y = min(self.current_y_values)
            max_y = max(self.current_y_values)

        # 固定ラインのY値も考慮
        min_y = min(min_y, 60)
        max_y = max(max_y, 60)

        # Y軸の範囲をキリの良い10刻みに調整
        # 最小値を10の倍数で切り捨て
        adjusted_min_y = (min_y // 10) * 10
        # 最大値を10の倍数で切り上げ
        adjusted_max_y = ((max_y + 9) // 10) * 10

        # Y軸の範囲を設定
        self.axis_y.setRange(adjusted_min_y, adjusted_max_y)

        # ティックカウントを動的に設定し、常に10刻みになるようにする
        tick_count = (adjusted_max_y - adjusted_min_y) // 10 + 1
        self.axis_y.setTickCount(tick_count)
        self.axis_y.setLabelFormat("%d") # 整数表示


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrendChartApp()
    window.show()
    sys.exit(app.exec())