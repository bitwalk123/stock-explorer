import sys
import random
import time # timeモジュールを追加
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QTimer, QPointF, Qt
from PySide6.QtGui import QPainter, QColor, QPen

class RealtimeChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイムトレンドチャート")
        self.setGeometry(100, 100, 800, 600)

        # メインウィジェットとレイアウト
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # チャートの作成
        self.chart = QChart()
        self.chart.setTitle("リアルタイムデータトレンド")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations) # 系列アニメーションを有効化

        # データ系列の作成
        self.series = QLineSeries()
        self.series.setName("ランダムデータ")
        self.chart.addSeries(self.series)

        # 固定ラインの作成 (y=60)
        self.fixed_line_series = QLineSeries()
        self.fixed_line_series.setName("閾値 (60)")
        pen = QPen(QColor(Qt.GlobalColor.red)) # 赤色
        pen.setWidth(2)
        self.fixed_line_series.setPen(pen)
        # 固定ラインのデータを設定 (横軸0から100まで)
        self.fixed_line_series.append(0, 60)
        self.fixed_line_series.append(100, 60)
        self.chart.addSeries(self.fixed_line_series)


        # X軸 (横軸) の設定
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 100)  # 0から100で範囲を固定
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTitleText("データポイント")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.fixed_line_series.attachAxis(self.axis_x) # 固定ラインもX軸にアタッチ

        # Y軸 (縦軸) の設定
        self.axis_y = QValueAxis()
        # Y軸の範囲は初期値として設定 (データ追加で動的に変更される)
        self.axis_y.setRange(0, 100)
        self.axis_y.setTickInterval(10) # 10刻みのティックラベル
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setTitleText("値")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        self.fixed_line_series.attachAxis(self.axis_y) # 固定ラインもY軸にアタッチ

        # QChartView の作成
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing) # アンチエイリアスを有効化
        layout.addWidget(self.chart_view)

        # データ関連の変数
        self.data_count = 0
        self.max_data_points = 100
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_data)
        self.timer.start(1000) # 1秒ごとにデータを追加

        # プロットされたY値のリスト (Y軸の動的なスケール調整用)
        self.y_values = []

    def add_data(self):
        if self.data_count >= self.max_data_points:
            self.timer.stop()
            print(f"データ追加を停止しました。合計 {self.data_count} 個のデータがプロットされました。")
            return

        start_time = time.perf_counter() # 処理開始時刻を記録

        # 0から100までのランダムな値を生成
        new_value = random.randint(0, 100)
        self.data_count += 1

        # 系列にデータを追加
        self.series.append(self.data_count, new_value)
        self.y_values.append(new_value)

        # Y軸のスケールを動的に調整
        self.update_y_axis_range()

        end_time = time.perf_counter() # 処理終了時刻を記録
        elapsed_time_ms = (end_time - start_time) * 1000 # ミリ秒に変換
        print(f"データポイント {self.data_count} の描画時間: {elapsed_time_ms:.4f} ms")


    def update_y_axis_range(self):
        if not self.y_values:
            return

        min_y = min(self.y_values)
        max_y = max(self.y_values)

        # 現在のY軸の範囲を取得
        current_min_y = self.axis_y.min()
        current_max_y = self.axis_y.max()

        # 閾値ライン(60)も考慮に入れる
        effective_min_y = min(min_y, 60)
        effective_max_y = max(max_y, 60)

        # 10の倍数に丸めて、少し余白を持たせる
        # 最小値を10の倍数で切り下げ、最大値を10の倍数で切り上げ
        new_min_y = (effective_min_y // 10) * 10
        new_max_y = ((effective_max_y + 9) // 10) * 10 # +9 してから切り上げで10の倍数に

        # Y軸の範囲が変更された場合のみ更新
        if new_min_y != current_min_y or new_max_y != current_max_y:
            # 最小値が最大値を超えないように調整
            if new_min_y >= new_max_y:
                if new_max_y == 0: # 例外的なケースでmax_yが0の場合
                    new_max_y = 10
                new_min_y = new_max_y - 10 if new_max_y - 10 >= 0 else 0


            self.axis_y.setRange(new_min_y, new_max_y)
            # print(f"Y軸範囲更新: [{new_min_y}, {new_max_y}]") # ベンチマークを邪魔しないようコメントアウト

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealtimeChart()
    window.show()
    sys.exit(app.exec())