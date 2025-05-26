import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtCharts import QChartView, QChart, QLineSeries
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QPointF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart_view = QChartView()
        self.setup_chart()

        save_button = QPushButton("Save as PNG")
        save_button.clicked.connect(self.save_chart_as_png)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("QChartView Save Example")

    def setup_chart(self):
        chart = QChart()
        series = QLineSeries()
        series.append(QPointF(0, 6))
        series.append(QPointF(2, 4))
        series.append(QPointF(3, 8))
        series.append(QPointF(7, 4))
        series.append(QPointF(10, 5))
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("Simple line chart")
        self.chart_view.setChart(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)  # 修正箇所

    def save_chart_as_png(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG Files (*.png)")
        if file_path:
            pixmap = self.chart_view.grab()
            pixmap.save(file_path, "png")
            print(f"プロットを {file_path} に保存しました。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())