import sys

import pandas as pd
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries, QScatterSeries, QValueAxis,
)
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from modules.psar import RealtimePSAR


class ChartView(QChartView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart = QChart()
        chart.setDropShadowEnabled(False)
        chart.legend().hide()
        self.setChart(chart)

        axis_x = QValueAxis()
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        name_excel = '../excel/trader_20250526.xlsx'
        df = pd.read_excel(name_excel, sheet_name='tick_7011')

        series_price = QLineSeries()
        for x, y in zip(df['Time'], df['Price']):
            series_price.append(x, y)
        chart.addSeries(series_price)
        series_price.attachAxis(axis_x)
        series_price.attachAxis(axis_y)

        list_trend = list()
        list_psar = list()

        psar = RealtimePSAR()
        for y in df['Price']:
            ret = psar.add(y)
            list_psar.append(ret.psar)
            list_trend.append(ret.trend)

        df['Trend'] = list_trend
        df['PSAR'] = list_psar

        series_bull = QScatterSeries()
        series_bull.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series_bull.setMarkerSize(5)
        series_bull.setPen(QPen(Qt.PenStyle.NoPen))
        df_bull = df[df['Trend'] == 1][['Time', 'PSAR']]
        for x, y in zip(df_bull['Time'], df_bull['PSAR']):
            series_bull.append(x, y)
        chart.addSeries(series_bull)
        series_bull.attachAxis(axis_x)
        series_bull.attachAxis(axis_y)

        series_bear = QScatterSeries()
        series_bear.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series_bear.setMarkerSize(5)
        series_bear.setPen(QPen(Qt.PenStyle.NoPen))
        df_bear = df[df['Trend'] == -1][['Time', 'PSAR']]
        for x, y in zip(df_bear['Time'], df_bear['PSAR']):
            series_bear.append(x, y)
        chart.addSeries(series_bear)
        series_bear.attachAxis(axis_x)
        series_bear.attachAxis(axis_y)

        #chart.createDefaultAxes()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1200, 400)
        chart_view = ChartView()
        self.setCentralWidget(chart_view)
        self.setWindowTitle('LineChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
