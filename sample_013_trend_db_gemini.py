import sys
import datetime
import time
import csv
import math
from collections import deque

# PySide6 のインポート
from PySide6.QtCore import (Qt, QTimer, QDateTime, QDate, QTime,
                            QThread, Signal, Slot, QMutex, QWaitCondition)
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlError


# --- データベース書き込みスレッドクラス (QThreadを使用、QSqlDatabase利用) ---
class DatabaseWriterThread(QThread):
    data_received = Signal(dict)

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self._queue = deque()
        self._mutex = QMutex()
        self._wait_condition = QWaitCondition()
        self._running = True
        self.COMMIT_INTERVAL_MS = 1000  # 1秒ごとにコミット
        self.BATCH_SIZE = 100  # または100件ごとにコミット

        self.data_received.connect(self.add_data)

    @Slot(dict)
    def add_data(self, data):
        self._mutex.lock()
        try:
            self._queue.append(data)
            self._wait_condition.wakeOne()
        finally:
            self._mutex.unlock()

    def run(self):
        conn_name = f"db_conn_{id(self)}"
        db = QSqlDatabase.addDatabase("QSQLITE", conn_name)
        db.setDatabaseName(self.db_path)

        if not db.open():
            print(f"データベース '{self.db_path}' への接続に失敗しました: {db.lastError().text()}")
            self._running = False
            return

        print(f"データベース '{self.db_path}' に接続しました。 (QThread with QSqlDatabase)")

        query = QSqlQuery(db)
        if not query.exec(f'''
            CREATE TABLE IF NOT EXISTS prices (
                timestamp INTEGER PRIMARY KEY,
                price REAL
            )
        '''):
            print(f"テーブル作成エラー: {query.lastError().text()}")
            db.close()
            self._running = False
            return

        insert_query = QSqlQuery(db)
        insert_query.prepare("INSERT INTO prices (timestamp, price) VALUES (:timestamp, :price)")

        last_commit_time = time.time()
        inserted_count = 0

        while self._running:
            self._mutex.lock()
            try:
                # キューが空の場合、データが来るまで待機
                # またはコミット間隔をチェックするために定期的に起こされる
                if not self._queue and (time.time() - last_commit_time) * 1000 < self.COMMIT_INTERVAL_MS:
                    self._wait_condition.wait(self._mutex, min(100, self.COMMIT_INTERVAL_MS - int(
                        (time.time() - last_commit_time) * 1000)))  # 待機時間を調整

                # コミット処理の開始（データがあるか、またはコミット間隔が経過した場合）
                if self._queue or (time.time() - last_commit_time) * 1000 >= self.COMMIT_INTERVAL_MS:
                    # トランザクションを開始
                    if not db.transaction():
                        print(f"トランザクション開始エラー: {db.lastError().text()}")
                        continue  # エラーの場合は次ループへ

                    while self._queue and inserted_count < self.BATCH_SIZE:
                        data = self._queue.popleft()

                        timestamp_unix = int(data["Time"].timestamp())
                        price = data["Price"]

                        insert_query.bindValue(":timestamp", timestamp_unix)
                        insert_query.bindValue(":price", price)

                        if not insert_query.exec():
                            print(f"データ挿入エラー: {insert_query.lastError().text()}")
                            # 挿入エラーが発生したら、トランザクションをロールバックして抜ける
                            db.rollback()
                            break  # while _queue ループを抜ける
                        inserted_count += 1

                    # コミット間隔が経過したか、バッチサイズに達したか、キューが空になった場合
                    if inserted_count > 0 or (time.time() - last_commit_time) * 1000 >= self.COMMIT_INTERVAL_MS:
                        if db.commit():
                            # print(f"DBコミット: {inserted_count}件") # デバッグ用
                            inserted_count = 0
                            last_commit_time = time.time()
                        else:
                            print(f"コミットエラー: {db.lastError().text()}")
                            db.rollback()  # コミット失敗時はロールバック

            except Exception as e:
                print(f"データベース処理エラー (QThread with QSqlDatabase): {e}")
                if db.transactionActive():  # トランザクションがアクティブならロールバック
                    db.rollback()
            finally:
                self._mutex.unlock()

        # スレッド終了前の最終コミット
        self._mutex.lock()  # キューに残っているデータを処理するために再度ロック
        try:
            if self._queue:  # 残りのデータをすべて処理
                if db.transaction():
                    remaining_count = 0
                    while self._queue:
                        data = self._queue.popleft()
                        timestamp_unix = int(data["Time"].timestamp())
                        price = data["Price"]
                        insert_query.bindValue(":timestamp", timestamp_unix)
                        insert_query.bindValue(":price", price)
                        if insert_query.exec():
                            remaining_count += 1
                        else:
                            print(f"最終データ挿入エラー: {insert_query.lastError().text()}")
                            db.rollback()
                            break
                    if db.commit():
                        print(f"最終コミット: {remaining_count}件")
                    else:
                        print(f"最終コミットエラー: {db.lastError().text()}")
                        db.rollback()
                else:
                    print(f"最終トランザクション開始エラー: {db.lastError().text()}")
        finally:
            self._mutex.unlock()

        db.close()
        QSqlDatabase.removeDatabase(conn_name)
        print(f"データベース '{self.db_path}' から切断しました。 (QThread with QSqlDatabase)")

    def stop_thread(self):
        self._running = False
        self._mutex.lock()
        try:
            self._wait_condition.wakeAll()
        finally:
            self._mutex.unlock()
        self.wait()

    # メインアプリケーションクラスは変更なし (長くなるため省略)


# RealtimeTrendChart クラスは、以前のコードから変更ありません。
# 上記の DatabaseWriterThread クラスだけを置き換えてください。

class RealtimeTrendChart(QMainWindow):
    def __init__(self, csv_file_path="sample.csv", db_file_path="trading_data.db", parent=None):
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

            # --- データベース書き込みスレッド関連の初期化 (QThread + QSqlDatabase版) ---
        self.db_file_path = db_file_path
        self.db_writer_thread = DatabaseWriterThread(self.db_file_path)
        self.db_writer_thread.start()

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

            self.db_writer_thread.data_received.emit(data_point)

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

        if max_y == min_y:
            min_y -= 50
            max_y += 50

        data_range = max_y - min_y

        tick_intervals = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        target_max_ticks = 5

        chosen_interval = tick_intervals[0]

        for interval in tick_intervals:
            num_ticks = math.ceil(data_range / interval) + 1

            if num_ticks <= target_max_ticks:
                chosen_interval = interval
                break
            elif interval == tick_intervals[-1]:
                chosen_interval = interval
                break

        min_y_rounded = math.floor(min_y / chosen_interval) * chosen_interval
        max_y_rounded = math.ceil(max_y / chosen_interval) * chosen_interval

        if min_y_rounded == max_y_rounded:
            min_y_rounded -= chosen_interval
            max_y_rounded += chosen_interval

        if min_y_rounded > max_y_rounded:
            min_y_rounded, max_y_rounded = max_y_rounded, min_y_rounded

        current_axis_min = self.axis_y.min()
        current_axis_max = self.axis_y.max()
        current_axis_interval = self.axis_y.tickInterval()

        if force_update or \
                min_y_rounded != current_axis_min or \
                max_y_rounded != current_axis_max or \
                chosen_interval != current_axis_interval:
            self.axis_y.setMin(min_y_rounded)
            self.axis_y.setMax(max_y_rounded)
            self.axis_y.setTickInterval(chosen_interval)

    def closeEvent(self, event):
        print("アプリケーション終了中...")
        if self.timer.isActive():
            self.timer.stop()

        if self.db_writer_thread and self.db_writer_thread.isRunning():
            print("データベース書き込みスレッドを停止中...")
            self.db_writer_thread.stop_thread()
            self.db_writer_thread.wait(5000)
            if self.db_writer_thread.isRunning():
                print("警告: データベース書き込みスレッドが時間内に終了しませんでした。")
            else:
                print("データベース書き込みスレッドが正常に終了しました。")

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    csv_file = "sample.csv"
    db_file = "trading_data.db"

    window = RealtimeTrendChart(csv_file_path=csv_file, db_file_path=db_file)
    window.show()
    sys.exit(app.exec())
