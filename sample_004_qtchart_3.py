"""
楽天証券マーケットスピードⅡ RSS で Excel 上に取得した株価データを
Python で読み込み株価トレンドをリアルタイムに描画するサンプル
"""
import os
import sys

import xlwings as xw
from PySide6.QtCore import QTime, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from widgets.views import TickView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Tick Data')
        self.resize(1000, 300)

        # 情報を取得する Excel ファイル
        name_excel = 'daytrader.xlsx'
        wb = xw.Book(name_excel)
        self.sheet = wb.sheets['Sheet1']

        # 列情報
        self.col_code = 0
        self.col_name = 1
        self.col_date = 2
        self.col_time = 3
        self.col_price = 4
        self.col_price_prev = 5

        # 時差と市場時間
        self.msec_delta = 9 * 60 * 60 * 1000
        self.t_start = QTime(9, 0, 0)
        self.t_end = QTime(15, 30, 0)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # ユーザー・インターフェイス
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        """
        チャート用インスタンス
        リアルタイムでプロットを更新するには、
        Matplotlib より QChart を利用した方が簡単にできる。
        """
        self.view = view = TickView()
        self.setCentralWidget(view)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # タイマー
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.timer = timer = QTimer()
        timer.timeout.connect(self.on_update_data)
        timer.setInterval(1000)
        self.timer.start()

    def on_update_data(self):
        # 現在時刻
        t_current = QTime.currentTime()
        # Excel シートから株価情報を取得
        p_current = self.sheet[1, self.col_price].value

        if self.t_start <= t_current <= self.t_end:
            # msec の数値へ変換すると UTC になってしまうため時差を調整
            x = t_current.msecsSinceStartOfDay() - self.msec_delta
            y = float(p_current)
            self.view.appendPoint(x, y)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
