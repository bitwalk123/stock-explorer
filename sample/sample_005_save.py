from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # QChartとQChartViewのセットアップ
        self.chart = QChart()
        self.chart.setTitle("Sample Chart")
        self.series = QLineSeries()
        self.series.append(0, 0)
        self.series.append(1, 1)
        self.series.append(2, 4)
        self.series.append(3, 9)
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()

        self.chart_view = QChartView(self.chart)

        # レイアウト設定
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.chart_view)
        self.setCentralWidget(central_widget)

        # PNG保存
        self.save_chart_as_png("chart_output.png")

    def save_chart_as_png(self, file_path):
        # QChartViewの内容をQPixmapとして取得
        pixmap = self.chart_view.grab()
        # QPixmapをPNG形式で保存
        pixmap.save(file_path, "PNG")
        print(f"Chart saved as {file_path}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

