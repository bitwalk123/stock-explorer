import sys
import datetime

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import QDateTime, Qt, QDate, QTime, QMargins
from PySide6.QtGui import QPainter


class StaticTrendChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QChart 時間軸フォーマット確認用サンプル")

        # 1. チャートの初期化
        self.chart = chart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setMargins(QMargins(0, 0, 0, 0))
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setTitle("銘柄名 (コード)")

        # 2. ダミーシリーズの追加 (軸を表示するためには少なくとも1つのシリーズが必要)
        # データは追加しないが、軸を可視化するために必要
        self.dummy_series = dummy_series = QLineSeries()
        chart.addSeries(dummy_series)

        # 3. X軸 (時間軸) の設定
        self.axis_x = axis_x = QDateTimeAxis()
        axis_x.setFormat("hh:mm")  # ティックラベルの表示フォーマット

        # 今日の日付を取得
        today = datetime.date.today()
        day_today = QDate(today.year, today.month, today.day)

        # 始点と終点の設定 (今日の日付データを使用)
        start_dt = QDateTime(day_today, QTime(8, 45, 0))
        end_dt = QDateTime(day_today, QTime(15, 30, 0))

        axis_x.setMin(QDateTime(start_dt))
        axis_x.setMax(QDateTime(end_dt))

        # ティックラベルとグリッド線
        axis_x.setTickCount(28)

        font_x = axis_x.labelsFont()
        font_x.setPixelSize(9)
        axis_x.setLabelsFont(font_x)

        axis_x.setTitleVisible(False)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        dummy_series.attachAxis(axis_x)

        # 4. Y軸 (数値軸) の設定
        self.axis_y = axis_y = QValueAxis()
        axis_y.setRange(0, 100)  # Y軸の範囲を固定
        axis_y.setTitleVisible(False)

        font_y = axis_y.labelsFont()
        font_y.setPixelSize(9)
        axis_y.setLabelsFont(font_y)

        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        dummy_series.attachAxis(axis_y)

        # 5. QChartView の設定
        self.chart_view = chart_view = QChartView(chart)
        chart_view.setFixedSize(1000, 200)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(chart_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StaticTrendChart()
    window.show()
    sys.exit(app.exec())
