import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QColor
import numpy as np
from scipy.interpolate import UnivariateSpline

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # サンプルデータ (SciPy で生成)
        x = np.linspace(-3, 3, 50)
        y_exact = np.exp(-x**2)
        y_noisy = y_exact + np.random.normal(0, 0.1, 50)
        spl_interp = UnivariateSpline(x, y_noisy, s=0)
        y_interp = spl_interp(x)
        spl_smooth = UnivariateSpline(x, y_noisy, s=1)
        y_smooth = spl_smooth(x)
        spl_smoother = UnivariateSpline(x, y_noisy, s=5)
        y_smoother = spl_smoother(x)

        # チャートの作成
        chart = QChart()
        chart.legend().setVisible(True)
        chart.setTitle("UnivariateSpline の例 (PySide6 QChart)")

        # シリーズの作成とデータ追加
        series_noisy = QLineSeries()
        series_noisy.setName("ノイズありデータ")
        for xv, yv in zip(x, y_noisy):
            series_noisy.append(QPointF(xv, yv))
        chart.addSeries(series_noisy)

        series_exact = QLineSeries()
        series_exact.setName("真の曲線")
        for xv, yv in zip(x, y_exact):
            series_exact.append(QPointF(xv, yv))
        chart.addSeries(series_exact)

        series_interp = QLineSeries()
        series_interp.setName("補間スプライン (s=0)")
        for xv, yv in zip(x, y_interp):
            series_interp.append(QPointF(xv, yv))
        chart.addSeries(series_interp)

        series_smooth = QLineSeries()
        series_smooth.setName("平滑化スプライン (s=1)")
        for xv, yv in zip(x, y_smooth):
            series_smooth.append(QPointF(xv, yv))
        chart.addSeries(series_smooth)

        series_smoother = QLineSeries()
        series_smoother.setName("平滑化スプライン (s=5)")
        for xv, yv in zip(x, y_smoother):
            series_smoother.append(QPointF(xv, yv))
        chart.addSeries(series_smoother)

        # 軸の作成と設定
        axis_x = QValueAxis()
        axis_x.setTitleText("x")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series_noisy.attachAxis(axis_x)
        series_exact.attachAxis(axis_x)
        series_interp.attachAxis(axis_x)
        series_smooth.attachAxis(axis_x)
        series_smoother.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("y")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series_noisy.attachAxis(axis_y)
        series_exact.attachAxis(axis_y)
        series_interp.attachAxis(axis_y)
        series_smooth.attachAxis(axis_y)
        series_smoother.attachAxis(axis_y)

        # チャートビューの作成と表示
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setCentralWidget(chart_view)
        self.setWindowTitle("UnivariateSpline の例 (PySide6 QChart)")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())