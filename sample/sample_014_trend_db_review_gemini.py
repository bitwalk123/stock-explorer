import sys
import datetime
import math

# PySide6 のインポート
from PySide6.QtCore import (Qt, QDateTime, QDate, QTime)
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlError


class ChartReviewApp(QMainWindow):
    def __init__(self, db_file_path="trading_data.db", parent=None):
        super().__init__(parent)
        self.setWindowTitle("トレンドデータレビューチャート")
        self.setGeometry(100, 100, 1200, 600)  # レビューのため少し大きめに設定

        self.chart = QChart()
        self.chart.setTitle("価格トレンドデータ")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.legend().hide()

        self.series = QLineSeries()
        self.series.setName("Price")
        self.chart.addSeries(self.series)

        # X軸 (時刻軸) の設定
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("h:mm")  # 横軸のフォーマットは "h:mm"
        self.axis_x.setTitleText("時刻")
        font = QFont("Monospace")
        self.axis_x.setLabelsFont(font)

        # --- X軸の範囲を9:00から15:30に固定 ---
        # データベース内のデータの日付が何であっても、表示上は当日として扱うためのダミーの日付
        today = datetime.date.today()
        start_date = QDate(today.year, today.month, today.day)
        end_date = QDate(today.year, today.month, today.day)

        self.start_time_q = QTime(9, 0, 0)
        self.end_time_q = QTime(15, 30, 0)

        start_datetime_q = QDateTime(start_date, self.start_time_q)
        end_datetime_q = QDateTime(end_date, self.end_time_q)

        self.axis_x.setMin(start_datetime_q)
        self.axis_x.setMax(end_datetime_q)

        self.axis_x.setTickCount(14)  # 9:00, 9:30, ..., 15:30 で14ティック
        # ----------------------------------------

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Y軸 (価格軸) の設定
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("価格")
        self.axis_y.setLabelFormat("%.0f")
        self.axis_y.setLabelsFont(font)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.axis_y.setTickType(QValueAxis.TickType.TicksDynamic)  # 動的調整

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.chart_view)

        # 価格の最小値・最大値追跡用 (Y軸の自動スケールに利用)
        self._min_price = float('inf')
        self._max_price = float('-inf')
        # 時刻の最小値・最大値追跡用 (Y軸の動的調整ロジックで必要だが、X軸固定のため直接X軸設定には利用しない)
        self._min_time_msecs = float('inf')
        self._max_time_msecs = float('-inf')

        # データベース接続をクラスのメンバー変数として保持
        self.db_file_path = db_file_path
        # PySide6のQSqlDatabaseは、スレッドごとにユニークな接続名が必要
        # メインスレッドでの接続なので、このインスタンスIDでユニーク性を確保
        self.db_conn_name = f"review_db_conn_{id(self)}"
        self.db = QSqlDatabase.addDatabase("QSQLITE", self.db_conn_name)
        self.db.setDatabaseName(self.db_file_path)

        # データベース接続を開く
        if not self.db.open():
            QMessageBox.critical(self, "データベース接続エラー",
                                 f"データベース '{self.db_file_path}' への接続に失敗しました:\n{self.db.lastError().text()}")
            # 接続失敗時はチャート表示せずに終了。
            # QMainWindowのコンストラクタは続行されるが、データはロードされない。
            self.chart.removeAllSeries()
            self.series = QLineSeries()
            return

        print(f"データベース '{self.db_file_path}' に接続しました。")

        # データベースからデータをロードし、チャートに表示
        self.load_data_to_chart()

    def load_data_to_chart(self):
        """
        開かれているデータベース接続からデータを読み込み、チャートに表示します。
        """
        # QSqlQuery オブジェクトは、self.db (既に開かれた接続) を使用して作成
        query = QSqlQuery(self.db)

        # pricesテーブルからtimestampとpriceをtimestamp昇順で取得
        if not query.exec("SELECT timestamp, price FROM prices ORDER BY timestamp ASC"):
            QMessageBox.critical(self, "データベースクエリエラー",
                                 f"データ取得クエリの実行に失敗しました:\n{query.lastError().text()}")
            # エラー発生時はシリーズをクリアして続行 (closeEventでDB接続を閉じるため)
            self.chart.removeAllSeries()
            self.series = QLineSeries()
            return

        data_loaded = False
        while query.next():
            timestamp_unix = query.value(0)  # 1列目のtimestamp (INTEGER)
            price_val = query.value(1)  # 2列目のprice (REAL)

            # UNIXエポック秒からQDateTimeに変換
            # QDateTime.fromSecsSinceEpoch()はUTCとして扱うため、ローカルタイムに変換
            # データベースに保存されているtimestampがローカルタイムのUNIXエポック秒であれば、
            # fromSecsSinceEpoch(timestamp_unix, Qt.LocalTime) を使用することも検討
            # ここではデフォルトのQt.UTCを使用し、表示フォーマットで吸収
            q_datetime = QDateTime.fromSecsSinceEpoch(timestamp_unix)

            # QChartはミリ秒単位のX座標を期待するため変換
            time_msecs = q_datetime.toMSecsSinceEpoch()

            self.series.append(time_msecs, price_val)
            data_loaded = True

            # Y軸の範囲を更新
            self._min_price = min(self._min_price, price_val)
            self._max_price = max(self._max_price, price_val)

            # _min_time_msecs, _max_time_msecs は、Y軸の動的調整ロジックで必要となる
            # 最小・最大価格の計算のため、一応追跡しておく
            self._min_time_msecs = min(self._min_time_msecs, time_msecs)
            self._max_time_msecs = max(self._max_time_msecs, time_msecs)

        # QSqlQuery オブジェクトを明示的に破棄し、参照を解放
        # これにより、データベース接続が「使用中」であると見なされにくくなる
        del query

        if not data_loaded:
            QMessageBox.information(self, "データなし", "データベースにトレンドデータが見つかりませんでした。")
        else:
            # Y軸の範囲とティック間隔を、読み込んだデータ全体に基づいて調整
            self.update_y_axis(self._min_price, self._max_price, force_update=True)

        # ここではデータベース接続を閉じない。
        # アプリケーション終了時にcloseEventで処理する。

    def update_y_axis(self, min_y, max_y, force_update=False):
        """
        Y軸の表示範囲とティック間隔を、データの最小・最大価格に基づいて動的に調整します。
        """
        # データが全くない、または単一点の場合のデフォルト範囲
        if max_y == float('-inf') or min_y == float('inf') or max_y == min_y:
            min_y = 2800.0  # ある程度の固定値を設定
            max_y = 3000.0

        data_range = max_y - min_y

        # ティック間隔の候補リスト
        tick_intervals = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        target_max_ticks = 10  # 目標とするティックの最大数

        chosen_interval = tick_intervals[0]  # 初期値

        # 最適なティック間隔を探索
        for interval in tick_intervals:
            num_ticks = math.ceil(data_range / interval) + 1  # その間隔で何ティック必要か

            if num_ticks <= target_max_ticks:
                chosen_interval = interval
                break  # 目標ティック数以下になったら採用
            elif interval == tick_intervals[-1]:
                chosen_interval = interval  # 最後の候補ならそれを使う
                break

        # ティック間隔に合わせて軸の最小値・最大値を丸める
        min_y_rounded = math.floor(min_y / chosen_interval) * chosen_interval
        max_y_rounded = math.ceil(max_y / chosen_interval) * chosen_interval

        # 丸めた結果、範囲がゼロになった場合の調整 (例: 1点しかデータがない場合)
        if min_y_rounded == max_y_rounded:
            min_y_rounded -= chosen_interval
            max_y_rounded += chosen_interval

        # 範囲が逆転した場合の調整 (通常は起こらないが念のため)
        if min_y_rounded > max_y_rounded:
            min_y_rounded, max_y_rounded = max_y_rounded, min_y_rounded

        # 現在の軸の設定を取得
        current_axis_min = self.axis_y.min()
        current_axis_max = self.axis_y.max()
        current_axis_interval = self.axis_y.tickInterval()

        # 強制更新フラグがあるか、または設定が実際に変更される場合にのみ更新
        if force_update or \
                min_y_rounded != current_axis_min or \
                max_y_rounded != current_axis_max or \
                chosen_interval != current_axis_interval:
            self.axis_y.setMin(min_y_rounded)
            self.axis_y.setMax(max_y_rounded)
            self.axis_y.setTickInterval(chosen_interval)

    def closeEvent(self, event):
        """
        QMainWindowが閉じられる際に呼び出されるイベントハンドラ。
        アプリケーション終了時にデータベース接続を安全に終了させます。
        """
        print("アプリケーション終了中...")

        # self.dbが有効で、かつ開かれている場合にのみ処理を行う
        if self.db and self.db.isOpen():
            print(f"データベース '{self.db_file_path}' から切断中...")
            self.db.close()  # データベース接続を閉じる

            # Qtのデータベース接続リストからこの接続を削除
            # この時点でまだGUIオブジェクトが内部でDBリソースを参照していると
            # 「connection is still in use」警告が出る可能性がある。
            # しかし、プロセス終了時にはOSが全てをクリーンアップするため、
            # 実用上は無視できることが多い。
            QSqlDatabase.removeDatabase(self.db_conn_name)
            print(f"データベース '{self.db_file_path}' から切断しました。")

        event.accept()  # ウィンドウクローズイベントを受け入れ、アプリケーションを終了


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # データを読み込むデータベースファイル名
    db_file = "../trading_data.db"

    # アプリケーションウィンドウの作成と表示
    window = ChartReviewApp(db_file_path=db_file)
    window.show()

    # アプリケーションのイベントループを開始
    sys.exit(app.exec())