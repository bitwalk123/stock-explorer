import datetime as dt
import os
import sys
import yfinance as yf

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QWidget,
)

from structs.res import AppRes
from widgets.labels import LabelHeader


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
        name_ticker = 'PHLX Semiconductor'
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
        ticker = '^BSESN'
        name_ticker = 'ムンバイ S&P BSE SENSEX'
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

        lab_title = QLabel(name_ticker)
        lab_title.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab_title.setLineWidth(1)
        lab_title.setStyleSheet("""
            QLabel {
                padding-left: 0.1em;
                padding-right: 0.1em;
                font-family: monospace;
                background-color: %s;
            }
        """ % bcolor)
        layout.addWidget(lab_title, row, 0)

        lab_date = QLabel(date_prev)
        lab_date.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab_date.setLineWidth(1)
        lab_date.setStyleSheet('QLabel{font-family: monospace; background-color: %s}' % bcolor)
        layout.addWidget(lab_date, row, 1)

        lab_close = QLabel(price_close)
        lab_close.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab_close.setLineWidth(1)
        lab_close.setStyleSheet('QLabel{font-family: monospace; background-color: %s}' % bcolor)
        lab_close.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(lab_close, row, 2)

        lab_delta = QLabel(delta)
        lab_delta.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab_delta.setLineWidth(1)
        lab_delta.setStyleSheet('QLabel{font-family: monospace; background-color: %s}' % bcolor)
        lab_delta.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
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
