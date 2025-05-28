import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChartView, QLineSeries, QChart, QValueAxis, QScatterSeries
from PySide6.QtCore import QTimer, Qt, QMargins  # QMarginsをインポート
from PySide6.QtGui import QPainter, QColor


class TrendChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイム風トレンドグラフ (PySide6)")
        self.setGeometry(100, 100, 800, 600)

        self.chart = QChart()
        self.chart.setTitle("リアルタイムトレンド")

        # ★ ここから変更点 ★
        # チャートのコンテンツマージンを設定して、プロットエリアと軸の間に余白を追加
        # 左、上、右、下の順にマージンを指定
        self.chart.setContentsMargins(20, 20, 20, 20)  # 例として20ピクセルの余白を設定
        # レイアウトのマージンも同様に設定することで、より全体的な余白を確保
        # QChartのレイアウトは自動的に生成されるため、アクセスして設定
        self.chart.layout().setContentsMargins(0, 0, 0, 0)  # QChart自体のマージンをリセットし、setContentsMarginsを優先
        # あるいは、外側のQChartViewのレイアウトで調整する方法もある
        # ★ ここまで変更点 ★

        self.line_series = QLineSeries()
        self.line_series.setPointsVisible(False)
        self.line_series.setColor(QColor("#4682B4"))
        self.chart.addSeries(self.line_series)

        self.scatter_series = QScatterSeries()
        self.scatter_series.setMarkerSize(12)
        self.scatter_series.setColor(QColor("red"))
        self.scatter_series.setBorderColor(QColor("darkred"))
        self.chart.addSeries(self.scatter_series)

        # 軸の設定 (横軸は1から60まで固定)
        self.axis_x = QValueAxis()
        self.axis_x.setRange(1, 60)
        self.axis_x.setTitleText("X軸")

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 100)
        self.axis_y.setTitleText("Y軸 (乱数)")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.line_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_y)
        self.scatter_series.attachAxis(self.axis_x)
        self.scatter_series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.chart_view)
        self.setCentralWidget(central_widget)

        self.data_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)

    def update_chart(self):
        if self.data_count < 60:
            x_val = self.data_count + 1
            y_val = random.randint(10, 90)

            self.line_series.append(x_val, y_val)

            self.scatter_series.clear()
            self.scatter_series.append(x_val, y_val)

            self.data_count += 1
            print(f"プロットデータ: x={x_val}, y={y_val}")
        else:
            self.timer.stop()
            print("60点のデータプロットが完了しました。タイマーを停止します。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrendChartApp()
    window.show()
    sys.exit(app.exec())
