import os
import sys
import time

import xlwings as xw
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        # Excelシートからデータを読み込むときの試行回数
        self.max_retries = 3  # 最大リトライ回数
        self.retry_delay = 0.1  # リトライ間の遅延（秒）

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

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DayTrader')
 

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
