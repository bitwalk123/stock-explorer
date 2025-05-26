import sys
import yfinance as yf
import pandas as pd
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries, QDateTimeAxis, QValueAxis, QCandlestickSet


class StockChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日経平均株価ローソク足チャート (^N225) - 最終版")
        self.setGeometry(100, 100, 1200, 600)

        self.chart = QChart()
        self.chart.setTitle("日経平均株価 (^N225) 過去6ヶ月")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.legend().setVisible(False)

        self.series = QCandlestickSeries()
        self.series.setName("株価")
        self.series.setIncreasingColor(QColor(0, 150, 0))
        self.series.setDecreasingColor(QColor(255, 0, 0))

        self.chart.addSeries(self.series)

        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("MM/dd")
        self.axisX.setTitleText("日付")
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axisX)

        self.axisY = QValueAxis()
        self.axisY.setTitleText("株価")
        self.axisY.setLabelFormat("%.0f")
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.load_stock_data()

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(chart_view)

    def load_stock_data(self):
        ticker_symbol = "^N225"

        try:
            obj = yf.Ticker(ticker_symbol)
            data: pd.DataFrame = obj.history(period="6mo", interval="1d")

            if data.empty:
                print(f"株価データを取得できませんでした。データが空です。({ticker_symbol})")
                self.axisX.setMin(QDateTime.currentDateTime())
                self.axisX.setMax(QDateTime.currentDateTime().addDays(1))
                self.axisY.setMin(0)
                self.axisY.setMax(1)
                return

            min_price = float('inf')
            max_price = float('-inf')

            self.series.clear()

            for index, row in data.iterrows():
                index: pd.Timestamp
                timestamp_ms = int(index.timestamp() * 1000)

                open_price = row["Open"].item()
                high_price = row["High"].item()
                low_price = row["Low"].item()
                close_price = row["Close"].item()

                candle_set = QCandlestickSet(
                    open_price, high_price, low_price, close_price, timestamp_ms
                )
                self.series.append(candle_set)

                min_price = min(min_price, low_price)
                max_price = max(max_price, high_price)

            if not data.empty:
                min_timestamp: pd.Timestamp = data.index.min()
                max_timestamp: pd.Timestamp = data.index.max()
                self.axisX.setMin(QDateTime.fromSecsSinceEpoch(int(min_timestamp.timestamp())))
                self.axisX.setMax(QDateTime.fromSecsSinceEpoch(int(max_timestamp.timestamp())))

            if min_price != float('inf') and max_price != float('-inf'):
                padding = (max_price - min_price) * 0.05
                self.axisY.setMin(min_price - padding)
                self.axisY.setMax(max_price + padding)
            else:
                self.axisY.setMin(0)
                self.axisY.setMax(1)

        except Exception as e:
            print(f"データの取得または処理中にエラーが発生しました: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockChartApp()
    window.show()
    sys.exit(app.exec())