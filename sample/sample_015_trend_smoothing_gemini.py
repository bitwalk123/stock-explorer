import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCharts import QChartView, QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QColor, QFont, QPen, QPainter
from PySide6.QtCore import QTimer, QDateTime, QTime, QUrl, QLocale, Qt, QPointF
import csv
import os
import math
import time
from scipy.signal import savgol_filter
import numpy as np


class RealtimeTrendChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイムトレンドチャート")
        self.setGeometry(100, 100, 1000, 300)

        # 株価トレンドのシリーズ
        self.series = QLineSeries()
        self.series.setName("Price Trend")
        self.series.setColor(QColor(Qt.blue))

        # スムージング曲線のシリーズ
        self.smoothed_series = QLineSeries()
        self.smoothed_series.setName("Smoothed Trend")
        pen_smoothed = QPen(QColor(Qt.magenta))
        pen_smoothed.setWidth(2)
        self.smoothed_series.setPen(pen_smoothed)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.smoothed_series)
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setMargins(self.chart.margins())
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setPlotArea(self.chart.plotArea())
        self.chart.legend().hide()
        self.chart.setTheme(QChart.ChartThemeLight)

        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("h:mm")
        self.axis_x.setTitleText("")
        self.axis_x.setLabelsFont(QFont("Monospace"))
        self.axis_x.setTickCount(14)

        # X軸の固定範囲をクラス変数として保持
        current_date = QDateTime.currentDateTime().date()
        self.x_axis_start_datetime = QDateTime(current_date, QTime(9, 0, 0))
        self.x_axis_end_datetime = QDateTime(current_date, QTime(15, 30, 0))

        self.axis_x.setRange(self.x_axis_start_datetime, self.x_axis_end_datetime)

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.smoothed_series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("")
        self.axis_y.setLabelFormat("%.0f")
        self.axis_y.setLabelsFont(QFont("Monospace"))
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        self.smoothed_series.attachAxis(self.axis_y)

        # 固定ライン (前日終値)
        self.previous_close_line = QLineSeries()
        self.previous_close_value = 2909.0

        self.previous_close_line.append(self.x_axis_start_datetime.toMSecsSinceEpoch(), self.previous_close_value)
        self.previous_close_line.append(self.x_axis_end_datetime.toMSecsSinceEpoch(), self.previous_close_value)

        pen = QPen(QColor(Qt.red))
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        self.previous_close_line.setPen(pen)
        self.chart.addSeries(self.previous_close_line)
        self.previous_close_line.attachAxis(self.axis_x)
        self.previous_close_line.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)

        self.data = []
        self.current_data_index = 0

        self.current_y_min_display = float('inf')
        self.current_y_max_display = float('-inf')

        self.overall_min_price = float('inf')
        self.overall_max_price = float('-inf')

        self.Y_AXIS_UPDATE_THRESHOLD_PERCENT = 0.05

        # Savitzky-Golayフィルタのパラメータ
        self.window_length = 61
        self.polyorder = 3

        if self.window_length % 2 == 0:
            self.window_length += 1
        if self.polyorder >= self.window_length:
            self.polyorder = self.window_length - 2

        # 描画対象のデータ点数を制限するための内部リスト
        self._plot_data_raw = []  # (timestamp, price) のタプルのリスト
        self._plot_data_smoothed = []  # (timestamp, price) のタプルのリスト

        # X軸表示範囲のミリ秒単位での開始と終了時刻 (ここで確実に初期化)
        self.x_axis_start_msec = self.x_axis_start_datetime.toMSecsSinceEpoch()
        self.x_axis_end_msec = self.x_axis_end_datetime.toMSecsSinceEpoch()

        # CSVデータの読み込みをこれらの属性が初期化された後に行う
        self.load_csv_data("../sample.csv")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(50)

    def load_csv_data(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                try:
                    time_idx = header.index('Time')
                    price_idx = header.index('Price')
                except ValueError:
                    raise ValueError("CSVファイルに 'Time' または 'Price' 列が見つかりません。")

                for row in reader:
                    if len(row) > max(time_idx, price_idx):
                        try:
                            time_str = row[time_idx]
                            price = float(row[price_idx])

                            dt = None
                            if len(time_str.split(':')) == 3:
                                dt = QDateTime.fromString(
                                    QDateTime.currentDateTime().toString("yyyy-MM-dd") + " " + time_str,
                                    "yyyy-MM-dd HH:mm:ss")
                            elif len(time_str.split(':')) == 2:
                                dt = QDateTime.fromString(
                                    QDateTime.currentDateTime().toString("yyyy-MM-dd") + " " + time_str + ":00",
                                    "yyyy-MM-dd HH:mm:ss")

                            if dt and dt.isValid():
                                # CSV読み込み時にX軸範囲のフィルタリングは行わない
                                # 全ての有効なデータを self.data に追加する
                                self.data.append((dt.toMSecsSinceEpoch(), price))
                            else:
                                print(f"Warning: 無効な時刻フォーマットが検出されました: {time_str}")
                        except ValueError:
                            print(f"Warning: 数値変換エラーまたはデータ欠損: {row}")
                    else:
                        print(f"Warning: 不正な行データ: {row}")
            if not self.data:
                raise ValueError("CSVファイルに有効なデータがありません。")

        except FileNotFoundError:
            QMessageBox.critical(self, "エラー", f"CSVファイル '{filename}' が見つかりません。")
            sys.exit(1)
        except ValueError as e:
            QMessageBox.critical(self, "エラー", f"CSVファイルの読み込みエラー: {e}")
            sys.exit(1)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"予期せぬエラーが発生しました: {e}")
            sys.exit(1)

    def update_chart(self):
        start_time_benchmark = time.perf_counter()

        if self.current_data_index < len(self.data):
            timestamp, price = self.data[self.current_data_index]

            # --- 生データの処理 ---
            self._plot_data_raw.append(QPointF(timestamp, price))

            # X軸の範囲外の古いデータを削除 (表示範囲の最小値より古いもの)
            # ここで self.axis_x.min().toMSecsSinceEpoch() を使用する
            while self._plot_data_raw and self._plot_data_raw[0].x() < self.axis_x.min().toMSecsSinceEpoch():
                self._plot_data_raw.pop(0)

            self.series.replace(self._plot_data_raw)

            # 全体の最小値・最大値を更新（表示されているデータのみを考慮）
            self.overall_min_price = min(p.y() for p in self._plot_data_raw) if self._plot_data_raw else float('inf')
            self.overall_max_price = max(p.y() for p in self._plot_data_raw) if self._plot_data_raw else float('-inf')

            # --- スムージングデータの処理 ---
            # フィルタリングに使う価格リスト (_plot_data_raw から抽出)
            prices_for_filter = [p.y() for p in self._plot_data_raw]

            if len(prices_for_filter) >= self.window_length:
                np_prices = np.array(prices_for_filter)

                # savgol_filterは窓の長さに応じて、入力配列の長さと同じ出力を返す
                # mode='interp' は端点処理を行い、出力の長さが入力と同じになる
                smoothed_full_y = savgol_filter(np_prices, self.window_length, self.polyorder, mode='interp')

                # _plot_data_smoothed を現在の表示範囲のデータで更新
                # _plot_data_raw と smoothed_full_y は同じインデックスに対応するため、まとめて QPointF を作成
                self._plot_data_smoothed = []
                for i in range(len(self._plot_data_raw)):
                    self._plot_data_smoothed.append(QPointF(self._plot_data_raw[i].x(), smoothed_full_y[i]))

                self.smoothed_series.replace(self._plot_data_smoothed)

                # スムージング後のデータも全体の範囲に含める
                # 表示されているスムージングデータのみから最小値・最大値を更新
                self.overall_min_price = min(self.overall_min_price, min(
                    p.y() for p in self._plot_data_smoothed) if self._plot_data_smoothed else float('inf'))
                self.overall_max_price = max(self.overall_max_price, max(
                    p.y() for p in self._plot_data_smoothed) if self._plot_data_smoothed else float('-inf'))
            else:
                # 窓の長さが揃うまではスムージング曲線は描画しない（または表示しない）
                self.smoothed_series.clear()

            # Y軸表示範囲の更新チェック
            update_needed = False
            # Y軸の範囲計算に利用する最小値・最大値を現在表示されているデータから算出
            current_displayed_min_y = float('inf')
            current_displayed_max_y = float('-inf')

            if self._plot_data_raw:
                current_displayed_min_y = min(current_displayed_min_y, min(p.y() for p in self._plot_data_raw))
                current_displayed_max_y = max(current_displayed_max_y, max(p.y() for p in self._plot_data_raw))
            if self._plot_data_smoothed:
                current_displayed_min_y = min(current_displayed_min_y, min(p.y() for p in self._plot_data_smoothed))
                current_displayed_max_y = max(current_displayed_max_y, max(p.y() for p in self._plot_data_smoothed))

            if current_displayed_min_y == float('inf') or current_displayed_min_y == current_displayed_max_y:
                update_needed = True
            else:
                range_width = self.current_y_max_display - self.current_y_min_display
                if range_width == 0:
                    update_needed = True
                else:
                    min_threshold_display = self.current_y_min_display + range_width * self.Y_AXIS_UPDATE_THRESHOLD_PERCENT
                    max_threshold_display = self.current_y_max_display - range_width * self.Y_AXIS_UPDATE_THRESHOLD_PERCENT

                    if not (
                            min_threshold_display <= current_displayed_min_y and current_displayed_max_y <= max_threshold_display):
                        update_needed = True

            if update_needed:
                self.update_y_axis_range(current_displayed_min_y, current_displayed_max_y)

            self.current_data_index += 1
        else:
            self.timer.stop()
            print("CSVデータの読み込みが完了しました。")

        end_time_benchmark = time.perf_counter()
        elapsed_time_ms = (end_time_benchmark - start_time_benchmark) * 1000
        print(f"1データ描画あたりの処理時間 ({self.current_data_index}/{len(self.data)}): {elapsed_time_ms:.3f} ms")

    def update_y_axis_range(self, current_min_data, current_max_data):
        current_min = current_min_data
        current_max = current_max_data

        if current_min == float('inf') or current_max == float('-inf') or current_min == current_max:
            self.axis_y.setRange(self.previous_close_value - 50, self.previous_close_value + 50)
            self.axis_y.setTickInterval(20)
            self.current_y_min_display = self.previous_close_value - 50
            self.current_y_max_display = self.previous_close_value + 50
            return

        min_val_with_fixed = min(current_min, self.previous_close_value)
        max_val_with_fixed = max(current_max, self.previous_close_value)

        price_range = max_val_with_fixed - min_val_with_fixed

        tick_intervals = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
        best_interval = 1
        min_tick_diff = float('inf')

        for interval in tick_intervals:
            num_ticks = price_range / interval
            diff = abs(num_ticks - 5)
            if diff < min_tick_diff and num_ticks > 0:
                min_tick_diff = diff
                best_interval = interval

        padding_factor = 0.1
        padding = max(best_interval * 2, price_range * padding_factor)

        new_min = math.floor((min_val_with_fixed - padding) / best_interval) * best_interval
        new_max = math.ceil((max_val_with_fixed + padding) / best_interval) * best_interval

        if new_min == new_max:
            new_max = new_min + best_interval

        if not (math.isclose(self.current_y_min_display, new_min) and math.isclose(self.current_y_max_display,
                                                                                   new_max)):
            self.axis_y.setRange(new_min, new_max)
            self.axis_y.setTickInterval(best_interval)
            self.current_y_min_display = new_min
            self.current_y_max_display = new_max


if __name__ == "__main__":
    app = QApplication(sys.argv)

    csv_filename = "../sample.csv"
    if not os.path.exists(csv_filename):
        print(f"'{csv_filename}' が見つかりません。テストデータを生成します。")
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Price"])
            current_time = QTime(9, 0, 0)
            price = 2900.0
            for i in range(18000):
                writer.writerow([current_time.toString("HH:mm:ss"), f"{price:.1f}"])
                current_time = current_time.addSecs(1)
                price_change = (math.sin(i / 100) * 20 + (i % 50 - 25)) * 0.05
                price += price_change
                if price < 2800: price = 2800
                if price > 3000: price = 3000

    window = RealtimeTrendChart()
    window.show()
    sys.exit(app.exec())