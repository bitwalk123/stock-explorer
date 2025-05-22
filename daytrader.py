import os
import sys
import time

if sys.platform == "win32":
    import xlwings as xw
    from pywintypes import com_error  # Windows 固有のライブラリ

    debug = False
else:
    debug = True

from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from funcs.tide import get_datetime_today
from structs.res import AppRes
from widgets.container import WidgetTicker
from widgets.layout import VBoxLayout


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        # Excelシートからデータを読み込むときの試行回数
        self.max_retries = 3  # 最大リトライ回数
        self.retry_delay = 0.1  # リトライ間の遅延（秒）

        #######################################################################
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
        self.col_lastclose = 5
        # 行情報
        self.num_max = 3
        #
        #######################################################################

        # ウィンドウ・タイトル
        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DayTrader')

        # 日付・時間情報
        self.dict_dt = dict_dt = get_datetime_today()

        layout = VBoxLayout()

        self.list_ticker = list_ticker = list()
        for num in range(self.num_max):
            row = num + 1

            # 指定銘柄
            ticker = WidgetTicker(row, res)
            # チャートのタイトル
            title = self.get_chart_title(row)
            ticker.setTitle(title)
            # X軸の範囲
            ticker.setTimeRange(dict_dt['start'], dict_dt['end'])
            # 前日の終値の横線
            p_lastclose = self.get_last_close(row)
            ticker.addLastCloseLine(p_lastclose)

            layout.addWidget(ticker)
            list_ticker.append(ticker)

        base = QWidget()
        base.setLayout(layout)
        self.setCentralWidget(base)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # タイマー
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.timer = timer = QTimer()
        timer.timeout.connect(self.on_update_data)
        timer.setInterval(1000)
        self.timer.start()

    def get_chart_title(self, row: int) -> str:
        code = self.sheet[row, self.col_code].value
        name = self.sheet[row, self.col_name].value
        title = '%s (%s)' % (name, code)
        return title

    def get_last_close(self, row: int) -> float:
        p_lastclose = self.sheet[row, self.col_lastclose].value
        return p_lastclose

    def on_update_data(self):
        for ticker in self.list_ticker:
            row = ticker.getRow()
            # Excel シートから株価情報を取得
            for attempt in range(self.max_retries):
                try:
                    # Excel シートから株価データを取得
                    y = self.sheet[row, self.col_price].value
                    # ここでデータ取得に成功したらループを抜ける
                    # ... 成功時の処理 ...
                    if y > 0:
                        dt = QDateTime.currentDateTime()
                        if self.dict_dt['start'] <= dt <= self.dict_dt['end']:
                            ticker.appendPoint(dt, y)
                    break
                except com_error as e:
                    # com_error は Windows 固有
                    if attempt < self.max_retries - 1:
                        print(f"COM Error occurred, retrying... (Attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                    else:
                        print(f"COM Error occurred after {self.max_retries} attempts. Giving up.")
                        raise  # 最終的に失敗したら例外を再発生させる
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    raise  # その他の例外はそのまま発生させる
            # ... (読み込んだ株価を使ったトレンドチャート作成の処理) ...


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
