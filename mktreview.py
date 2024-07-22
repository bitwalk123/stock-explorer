import datetime as dt
import os
import sys

import yfinance as yf

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QScrollArea,
    QWidget,
)

from structs.res import AppRes
from widgets.labels import (
    LabelDateStr,
    LabelHeader,
    LabelTicker,
    LabelValueStr,
)


class MktReview(QMainWindow):
    def __init__(self):
        super().__init__()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'summary.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Market Review')

        area = QScrollArea()
        area.setWidgetResizable(True)
        self.setCentralWidget(area)

        base = QWidget()
        area.setWidget(base)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        base.setLayout(layout)

        date_end = dt.date.today()
        date_start = date_end + dt.timedelta(days=-14)

        row = 0
        self.add_header(layout, row)

        row += 1
        ticker = '^DJI'
        name_ticker = 'ダウ工業株30種平均'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^IXIC'
        name_ticker = 'ナスダック総合指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^GSPC'
        name_ticker = 'S&P500'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^SOX'
        name_ticker = 'PHLX Semiconductor (SOX)'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'NVDA'
        name_ticker = 'NVIDIA'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'AAPL'
        name_ticker = 'Apple'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'ASML'
        name_ticker = 'ASML Holding N.V.'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'TSM'
        name_ticker = 'TSMC'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'ARM'
        name_ticker = 'ARM Holdings PLC'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'MU'
        name_ticker = 'Micron'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'INTC'
        name_ticker = 'Intel'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'AMAT'
        name_ticker = 'Applied Materials'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'LRCX'
        name_ticker = 'Lam Research'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = 'TOELY'
        name_ticker = 'Tokyo Electron Ltd. (ADR)'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^FTSE'
        name_ticker = '英 FTSE 指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)


        row += 1
        ticker = '^GDAXI'
        name_ticker = '独 DAX 指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^FCHI'
        name_ticker = '仏 CAC 40 指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^BSESN'
        name_ticker = 'ムンバイ S&P BSE SENSEX'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '000001.SS'
        name_ticker = '上海総合指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^HSI'
        name_ticker = '香港ハンセン指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^TWII'
        name_ticker = '台湾加権指数'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)

        row += 1
        ticker = '^N225'
        name_ticker = '日経平均株価（日経225）'
        self.add_row(layout, row, date_start, date_end, ticker, name_ticker)


    def add_header(self, layout: QGridLayout, row: int):
        lab_title = LabelHeader('銘柄・指数')
        layout.addWidget(lab_title, row, 0)

        lab_date = LabelHeader('取引日')
        layout.addWidget(lab_date, row, 1)

        lab_close = LabelHeader('終値')
        layout.addWidget(lab_close, row, 2)

        lab_delta = LabelHeader('前日差')
        layout.addWidget(lab_delta, row, 3)

    def add_row(
            self,
            layout: QGridLayout,
            row: int,
            date_start: dt.date,
            date_end: dt.date,
            ticker: str,
            name_ticker: str
    ):
        date_prev, price_close, delta, bcolor = self.get_latest(ticker, date_start, date_end)

        lab_title = LabelTicker(name_ticker, bcolor)
        layout.addWidget(lab_title, row, 0)

        lab_date = LabelDateStr(date_prev, bcolor)
        layout.addWidget(lab_date, row, 1)

        lab_close = LabelValueStr(price_close, bcolor)
        layout.addWidget(lab_close, row, 2)

        lab_delta = LabelValueStr(delta, bcolor)
        layout.addWidget(lab_delta, row, 3)

    def get_latest(self, ticker, date_start, date_end):
        df = yf.download(ticker, date_start, date_end)
        date_prev = str(df.tail(1).index[0].date())
        price_close = '%.2f' % df.tail(2)['Adj Close'].iloc[1]
        delta = df.tail(2)['Adj Close'].iloc[1] - df.tail(2)['Adj Close'].iloc[0]
        delta_str = '%.2f' % delta
        if delta < 0:
            bcolor = '#efe'
        else:
            bcolor = '#fee'

        return date_prev, price_close, delta_str, bcolor


def main():
    app = QApplication()
    ex = MktReview()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
