import sys
import datetime
import time
import csv
import math  # math.floor, math.ceil を使用するために追加
from PySide6.QtCore import Qt, QTimer, QDateTime, QDate, QTime
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis


class RealtimeTrendChart(QMainWindow):
    def __init__(self, csv_file_path="sample.csv", parent=None):
        super().__init__(parent)
        self.setWindowTitle("リアルタイムトレンドチャート")
        self.setGeometry(100, 100, 1000, 300)

        self.chart = QChart()
        self.chart.setTitle("")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.legend().hide()

        self.series = QLineSeries()
        self.series.setName("Price")
        self.chart.addSeries(self.series)

        # X軸 (時刻軸) の設定
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("h:mm")
        self.axis_x.setTitleText("")

        font = QFont("Monospace")
        self.axis_x.setLabelsFont(font)

        today = datetime.date.today()
        start_date = QDate(today.year, today.month, today.day)
        end_date = QDate(today.year, today.month, today.day)

        self.start_time_q = QTime(9, 0, 0)
        self.end_time_q = QTime(15, 30, 0)

        start_datetime_q = QDateTime(start_date, self.start_time_q)
        end_datetime_q = QDateTime(end_date, self.end_time_q)

        self.axis_x.setMin(start_datetime_q)
        self.axis_x.setMax(end_datetime_q)

        self.axis_x.setTickCount(14)

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Y軸 (価格軸) の設定
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("")
        self.axis_y.setLabelFormat("%.0f")
        self.axis_y.setLabelsFont(font)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.axis_y.setTickType(QValueAxis.TickType.TicksDynamic)

        self._current_min_y = 2909.0
        self._current_max_y = 2909.0

        self.prev_close_line = QLineSeries()
        self.prev_close_line.setName("前日終値")
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        self.prev_close_line.setPen(pen)

        self.prev_close_line.append(start_datetime_q.toMSecsSinceEpoch(), 2909.0)
        self.prev_close_line.append(end_datetime_q.toMSecsSinceEpoch(), 2909.0)

        self.chart.addSeries(self.prev_close_line)
        self.prev_close_line.attachAxis(self.axis_x)
        self.prev_close_line.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.chart_view)

        self.data_index = 0
        self.chart_data = []
        if not self.load_data_from_csv(csv_file_path):
            QMessageBox.critical(self, "エラー",
                                 f"CSVファイルの読み込みに失敗しました: {csv_file_path}\nアプリケーションを終了します。")
            sys.exit(1)

        if self.chart_data:
            initial_price = self.chart_data[0]["Price"]
            self._current_min_y = min(self._current_min_y, initial_price)
            self._current_max_y = max(self._current_max_y, initial_price)
            self.update_y_axis(force_update=True)

        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start()

    def load_data_from_csv(self, file_path):
        temp_data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'Time' not in reader.fieldnames or 'Price' not in reader.fieldnames:
                    print("CSVファイルに 'Time' または 'Price' 列が見つかりません。")
                    return False

                today = datetime.date.today()

                for row in reader:
                    try:
                        time_str = row['Time']

                        if len(time_str.split(':')) == 3:
                            time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
                        else:
                            time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()

                        full_datetime = datetime.datetime(today.year, today.month, today.day,
                                                          time_obj.hour, time_obj.minute, time_obj.second)

                        price_val = float(row['Price'])
                        temp_data.append({"Time": full_datetime, "Price": price_val})
                    except ValueError as e:
                        print(f"CSVデータのパースエラー: {row} - {e}")
                        continue

            self.chart_data = sorted(temp_data, key=lambda x: x["Time"])
            return True
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return False
        except Exception as e:
            print(f"CSV読み込み中に予期せぬエラーが発生しました: {e}")
            return False

    def update_chart(self):
        if self.data_index < len(self.chart_data):
            start_time_benchmark = time.perf_counter()

            data_point = self.chart_data[self.data_index]
            time_val_py = data_point["Time"]
            price_val = data_point["Price"]

            self._current_min_y = min(self._current_min_y, price_val)
            self._current_max_y = max(self._current_max_y, price_val)

            q_date = QDate(time_val_py.year, time_val_py.month, time_val_py.day)
            q_time = QTime(time_val_py.hour, time_val_py.minute, time_val_py.second, time_val_py.microsecond // 1000)

            time_msecs = QDateTime(q_date, q_time).toMSecsSinceEpoch()

            self.series.append(time_msecs, price_val)

            self.update_y_axis()

            end_time_benchmark = time.perf_counter()
            processing_time_ms = (end_time_benchmark - start_time_benchmark) * 1000
            print(f"データ追加処理時間: {processing_time_ms:.2f} ms")

            self.data_index += 1
        else:
            self.timer.stop()
            print("すべてのデータのプロットが完了しました。")

    def update_y_axis(self, force_update=False):
        min_y = self._current_min_y
        max_y = self._current_max_y

        # Y軸の範囲が極端に狭い場合（データが1点だけなど）の対応
        if max_y == min_y:
            min_y -= 50  # ある程度の範囲を確保
            max_y += 50

        data_range = max_y - min_y

        # 刻み幅の候補と、目標のティックラベル数
        tick_intervals = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]  # より大きな刻みも追加
        target_max_ticks = 5  # 目標とする最大ティック数

        chosen_interval = tick_intervals[0]  # デフォルトは10

        # 最適な刻み幅を探索
        for interval in tick_intervals:
            # ティックの概算数 (データ範囲 / 刻み幅)。端数も考慮して1を足す。
            num_ticks = math.ceil(data_range / interval) + 1

            if num_ticks <= target_max_ticks:
                chosen_interval = interval
                break
            # もしこのintervalでティックが多すぎる場合は、次の大きなintervalを試す
            # ただし、最後のintervalまで来てしまった場合は、そのintervalを使う
            elif interval == tick_intervals[-1]:
                chosen_interval = interval
                break

        # 刻み幅に合わせてY軸の表示範囲を調整
        min_y_rounded = math.floor(min_y / chosen_interval) * chosen_interval
        max_y_rounded = math.ceil(max_y / chosen_interval) * chosen_interval

        # 範囲が小さすぎて min_y_rounded == max_y_rounded になってしまう場合の調整
        if min_y_rounded == max_y_rounded:
            min_y_rounded -= chosen_interval
            max_y_rounded += chosen_interval

        # 値が逆転しないように保証
        if min_y_rounded > max_y_rounded:
            min_y_rounded, max_y_rounded = max_y_rounded, min_y_rounded

        current_axis_min = self.axis_y.min()
        current_axis_max = self.axis_y.max()
        current_axis_interval = self.axis_y.tickInterval()  # 現在の刻み幅も取得

        # 変更があった場合のみ更新
        if force_update or \
                min_y_rounded != current_axis_min or \
                max_y_rounded != current_axis_max or \
                chosen_interval != current_axis_interval:  # 刻み幅も比較対象に追加

            self.axis_y.setMin(min_y_rounded)
            self.axis_y.setMax(max_y_rounded)
            self.axis_y.setTickInterval(chosen_interval)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    csv_file = "../sample.csv"

    window = RealtimeTrendChart(csv_file_path=csv_file)
    window.show()
    sys.exit(app.exec())