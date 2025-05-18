import sys

import pandas as pd
import xlwings as xw
from PySide6.QtCore import QTime, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from widgets.views import TickView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        self.df = pd.DataFrame()
        self.row = 0
        self.length = 0
        self.msec_delta = 9 * 60 * 60 * 1000
        self.resize(1000, 500)

        name_excel = 'daytrader.xlsx'
        wb = xw.Book(name_excel)
        self.sheet = wb.sheets['Sheet1']

        self.col_code = 0
        self.col_name = 1
        self.col_date = 2
        self.col_time = 3
        self.col_price = 4
        self.col_price_prev = 5

        self.msec_delta = 9 * 60 * 60 * 1000
        self.t_start = QTime(9, 0, 0)
        self.t_end = QTime(15, 30, 0)

        self.view = view = TickView()
        self.setCentralWidget(view)

        self.timer = timer = QTimer()
        timer.timeout.connect(self.on_update_data)
        timer.setInterval(1000)
        self.timer.start()

    def on_update_data(self):
        t_current = QTime.currentTime()
        p_current = self.sheet[1, self.col_price].value

        if self.t_start <= t_current <= self.t_end:
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
