import os
import sys
import time

import xlwings as xw
from PySide6.QtCharts import QLineSeries, QChartView
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from structs.res import AppRes
from widgets.buttons import ToolButtonSave
from widgets.charts import Chart, MarketTimeAxis, PriceAxis
from widgets.layout import VBoxLayout
from widgets.toolbar import ToolBar


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        # Excelシートからデータを読み込むときの試行回数
        self.max_retries = 3  # 最大リトライ回数
        self.retry_delay = 0.1  # リトライ間の遅延（秒）

        # 情報を取得する Excel ファイル
        name_excel = 'daytrader.xlsx'
        wb = xw.Book(name_excel)
        self.sheet = wb.sheets['Sheet1']

        # 列情報
        self.col_code = 0
        self.col_name = 1
        self.col_date = 2
        self.col_time = 3
        self.col_price = 4
        self.col_lastclose = 5

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DayTrader')

        series = QLineSeries()
        chart = Chart()
        chart.setMinimumSize(1000, 300)
        chart.addSeries(series)

        axis_x = MarketTimeAxis()
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Y軸（株価）
        axis_y = PriceAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView()
        chart_view.setChart(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        toolbar = ToolBar()
        but_save = ToolButtonSave(self.res)
        # but_save.clicked.connect(view.saveChart)
        toolbar.addWidget(but_save)

        layout = VBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(chart_view)

        base = QWidget()
        base.setLayout(layout)
        self.setCentralWidget(base)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
