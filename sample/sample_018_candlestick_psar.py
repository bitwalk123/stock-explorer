import sys
import yfinance as yf
import pandas as pd
import numpy as np

from PySide6.QtCore import Qt, QDateTime, QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QCandlestickSeries,
    QCandlestickSet,
    QDateTimeAxis,
    QScatterSeries,
    QValueAxis,
)


def psar(ohlc: pd.DataFrame, iaf: float = 0.02, maxaf: float = 0.2) -> dict:
    """
    Parabolic SAR を計算します。
    Args:
        ohlc (pd.DataFrame): OHLCV データを含むDataFrame ('High', 'Low', 'Close' カラムが必要)
        iaf (float): 初期加速因子 (Initial Acceleration Factor)
        maxaf (float): 最大加速因子 (Maximum Acceleration Factor)
    Returns:
        dict: 'bear' (下降トレンドのSAR) と 'bull' (上昇トレンドのSAR) をキーとする
              numpy 配列を含む辞書。SAR値がない場合はNone/NaNが含まれます。
    """
    length = len(ohlc)
    high = ohlc['High'].tolist()
    low = ohlc['Low'].tolist()
    close = ohlc['Close'].tolist()

    # psarリストをcloseと同じ長さで初期化。最初の値はNaNで開始することが一般的ですが、
    # ご提示のコードではclose[0:len(close)]で初期化されています。
    # 実際の計算はインデックス2から始まるため、最初の2つの値は後で調整が必要かもしれません。
    psar_values = [None] * length  # psar_valuesという名前に変更して混乱を避ける
    psarbull = [None] * length
    psarbear = [None] * length

    # 初期トレンドとEPの設定
    # ご提示のコードでは、最初の2つの値が未定義のままループが2から始まります。
    # 一般的なPSARの実装では、最初のSARは最初の日の反対側の極値、EPは最初の日の極値から始めます。
    # ここではご提示のコードのロジックに従います。
    # 初期トレンドの決定とEPの設定
    # ここでご提示のコードのinitialization logicをそのまま再現します。
    # ただし、最初の2つのpsar値は計算されないため、psar_values[0]とpsar_values[1]はNoneのままになる可能性があります。
    # それらがNoneのままだとグラフに点が表示されないため、最初の有効なEP/SARで初期化します。

    # 初期のEPとSAR、トレンドの決定 (インデックス1のSARを計算するために必要)
    # これは psar 関数の中で、インデックス2からのループに備えるための準備です。
    # `close[0]`と`close[1]`を使って初期トレンドを決定します。
    if close[1] > close[0]:  # 上昇トレンドで開始
        bull = True
        ep = high[0]  # EPは初期高値
        psar_values[1] = low[0]  # SARは初期安値 (ただし、これはあくまで計算のためのシード値)
    else:  # 下降トレンドで開始
        bull = False
        ep = low[0]  # EPは初期安値
        psar_values[1] = high[0]  # SARは初期高値 (同上)

    af = iaf
    # price_highとprice_lowも初期化
    price_high = high[0]
    price_low = low[0]

    # 最初のSAR値はNaNか、または最初のEPを使用する実装もあるため、
    # ここではご提示のループ開始（インデックス2）に合わせるため、
    # インデックス0と1は計算されないまま、Noneのままで進めます。
    # 実際には、グラフに表示されるのはインデックス2以降の点になります。

    for i in range(2, length):
        # 以前のSAR値を使用
        prev_sar = psar_values[i - 1] if psar_values[i - 1] is not None else (
            low[i - 1] if bull else high[i - 1])  # もしpsar_values[i-1]がNoneなら直前の安値/高値を代用

        if bull:
            calculated_sar_today = prev_sar + af * (ep - prev_sar)
            # キャッピングルール：SARは現在の安値または前日の安値より高くなってはならない
            # ご提示のコードにはこのキャッピングが明示的に書かれていませんが、
            # 実際のPSARでは通常含まれます。ここではご提示のコードのロジックに忠実に従います。
        else:
            calculated_sar_today = prev_sar - af * (prev_sar - ep)
            # キャッピングルール：SARは現在の高値または前日の高値より低くなってはならない

        psar_values[i] = calculated_sar_today  # まずは暫定的なSARを設定

        reverse = False

        if bull:  # 現在上昇トレンド
            if low[i] < psar_values[i]:  # 価格がSARを下抜けた場合、トレンド反転
                bull = False
                reverse = True
                psar_values[i] = price_high  # 新しいSARは前のトレンドのEP
                price_low = low[i]  # 新しいEPは現在の安値
                af = iaf  # AFリセット
        else:  # 現在下降トレンド
            if high[i] > psar_values[i]:  # 価格がSARを上抜けた場合、トレンド反転
                bull = True
                reverse = True
                psar_values[i] = price_low  # 新しいSARは前のトレンドのEP
                price_high = high[i]  # 新しいEPは現在の高値
                af = iaf  # AFリセット

        if not reverse:  # トレンド継続の場合
            if bull:
                if high[i] > price_high:  # 新しい高値の場合、EPを更新しAF加速
                    price_high = high[i]
                    af = min(af + iaf, maxaf)
                # SARキャッピングルール (ご提示のコードに忠実)
                if low[i - 1] < psar_values[i]:
                    psar_values[i] = low[i - 1]
                if low[i - 2] < psar_values[i]:
                    psar_values[i] = low[i - 2]
            else:  # 下降トレンド継続
                if low[i] < price_low:  # 新しい安値の場合、EPを更新しAF加速
                    price_low = low[i]
                    af = min(af + iaf, maxaf)
                # SARキャッピングルール (ご提示のコードに忠実)
                if high[i - 1] > psar_values[i]:
                    psar_values[i] = high[i - 1]
                if high[i - 2] > psar_values[i]:
                    psar_values[i] = high[i - 2]

        # SARを対応するbull/bearリストに格納
        if bull:
            psarbull[i] = psar_values[i]
        else:
            psarbear[i] = psar_values[i]

    # インデックス0と1のデータは計算されていないので、Noneのままとなる
    # ただし、一般的にはpsar[0]とpsar[1]も初期値が入るか、NaNになる。
    # 今回のグラフ表示ではNoneはスキップされるので問題ない。

    return {
        'bear': np.array(psarbear, dtype='float64'),
        'bull': np.array(psarbull, dtype='float64'),
    }


class StockChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日経平均株価ローソク足チャート (^N225) - PSAR")
        self.setGeometry(100, 100, 1200, 600)

        self.chart = QChart()
        self.chart.setTitle("日経平均株価 (^N225) 過去6ヶ月")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.legend().setVisible(False)

        # ローソク足シリーズの設定
        self.series = QCandlestickSeries()
        self.series.setName("株価")
        self.series.setIncreasingColor(QColor(Qt.GlobalColor.white))
        self.series.setDecreasingColor(QColor(Qt.GlobalColor.black))
        candlestick_pen = QPen(Qt.GlobalColor.black)
        candlestick_pen.setWidth(1)
        self.series.setPen(candlestick_pen)
        self.chart.addSeries(self.series)

        # --- Parabolic SAR シリーズの設定 (上昇トレンド用: 赤の点) ---
        self.sar_bull_series = QScatterSeries()
        self.sar_bull_series.setName("PSAR (Up trend)")
        self.sar_bull_series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)  # 円形
        self.sar_bull_series.setMarkerSize(8)  # 点のサイズ
        self.sar_bull_series.setColor(QColor(Qt.GlobalColor.red))  # 赤色
        self.chart.addSeries(self.sar_bull_series)

        # --- Parabolic SAR シリーズの設定 (下降トレンド用: 青の点) ---
        self.sar_bear_series = QScatterSeries()
        self.sar_bear_series.setName("PSAR (Down trend)")
        self.sar_bear_series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)  # 円形
        self.sar_bear_series.setMarkerSize(8)  # 点のサイズ
        self.sar_bear_series.setColor(QColor(Qt.GlobalColor.blue))  # 青色
        self.chart.addSeries(self.sar_bear_series)
        # --- ここまで ---

        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("MM/dd")
        self.axisX.setTitleText("日付")
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axisX)
        self.sar_bull_series.attachAxis(self.axisX)  # 新しいSARシリーズもX軸にアタッチ
        self.sar_bear_series.attachAxis(self.axisX)  # 新しいSARシリーズもX軸にアタッチ

        self.axisY = QValueAxis()
        self.axisY.setTitleText("株価")
        self.axisY.setLabelFormat("%.0f")
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axisY)
        self.sar_bull_series.attachAxis(self.axisY)  # 新しいSARシリーズもY軸にアタッチ
        self.sar_bear_series.attachAxis(self.axisY)  # 新しいSARシリーズもY軸にアタッチ

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
            self.sar_bull_series.clear()  # SARシリーズのデータをクリア
            self.sar_bear_series.clear()  # SARシリーズのデータをクリア

            # --- ご提示いただいた psar 関数を呼び出し ---
            # pd.DataFrameを直接渡す
            psar_data = psar(data[['High', 'Low', 'Close']])
            bull_sar = psar_data['bull']
            bear_sar = psar_data['bear']
            # --- ここまで ---

            for i, (index, row) in enumerate(data.iterrows()):
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

                # --- PSARデータを QScatterSeries に追加 ---
                # psar関数の出力はnumpy配列でNoneが含まれるため、np.isnan でチェック
                if i < len(bull_sar) and not np.isnan(bull_sar[i]):
                    self.sar_bull_series.append(QPointF(timestamp_ms, bull_sar[i]))

                if i < len(bear_sar) and not np.isnan(bear_sar[i]):
                    self.sar_bear_series.append(QPointF(timestamp_ms, bear_sar[i]))
                # --- ここまで ---

                # 軸の最小・最大値にSAR値も考慮に入れる
                # SAR値はNoneやNaNになる可能性があるので、これらをフィルタリング
                current_sar_val = None
                if i < len(bull_sar) and not np.isnan(bull_sar[i]):
                    current_sar_val = bull_sar[i]
                elif i < len(bear_sar) and not np.isnan(bear_sar[i]):
                    current_sar_val = bear_sar[i]

                min_price = min(min_price, low_price, current_sar_val if current_sar_val is not None else float('inf'))
                max_price = max(max_price, high_price,
                                current_sar_val if current_sar_val is not None else float('-inf'))

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
            # エラー発生時は軸の表示をリセットするなど、ユーザーへのフィードバックを考慮
            self.axisX.setMin(QDateTime.currentDateTime().addDays(-7))
            self.axisX.setMax(QDateTime.currentDateTime())
            self.axisY.setMin(0)
            self.axisY.setMax(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockChartApp()
    window.show()
    sys.exit(app.exec())
