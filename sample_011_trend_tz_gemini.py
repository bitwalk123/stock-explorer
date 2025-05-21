from PySide6.QtCore import QTime, QDate, QDateTime, Qt, QTimeZone # QTimeZoneを追加
from PySide6.QtCharts import QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QChart
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

# 株価データと時刻データ（例）
stock_data = [
    ("09:00:00", 100),
    ("09:30:00", 105),
    ("10:00:00", 102),
    ("10:30:00", 108),
    ("11:00:00", 106),
    ("11:30:00", 110),
    ("12:00:00", 107),
    ("12:30:00", 109),
    ("13:00:00", 112),
    ("13:30:00", 110),
    ("14:00:00", 115),
    ("14:30:00", 113),
    ("15:00:00", 118),
]

app = QApplication(sys.argv)

series = QLineSeries()
dummy_date = QDate(2000, 1, 1) # ダミーの日付

for time_str, price in stock_data:
    q_time = QTime.fromString(time_str, "H:mm:ss")
    # QTimeZone.systemTimeZone() を使用してローカルタイムゾーンを明示的に指定
    q_datetime = QDateTime(dummy_date, q_time, QTimeZone.systemTimeZone())
    series.append(q_datetime.toMSecsSinceEpoch(), price)

chart = QChart()
chart.addSeries(series)
chart.setTitle("株価トレンドチャート (QDateTimeAxis使用)")

# X軸（時刻）- QDateTimeAxisを使用
axis_x = QDateTimeAxis()
axis_x.setFormat("h:mm") # ここで時刻フォーマットを設定
axis_x.setTitleText("時刻")
chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
series.attachAxis(axis_x)

# Y軸（株価）
axis_y = QValueAxis()
axis_y.setTitleText("株価")
chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
series.attachAxis(axis_y)

chart_view = QChartView(chart)
chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

main_window = QMainWindow()
main_window.setCentralWidget(chart_view)
main_window.resize(800, 600)
main_window.setWindowTitle("株価トレンドチャート (QDateTimeAxis)")
main_window.show()

sys.exit(app.exec())