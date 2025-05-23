import os
import sys

import yfinance as yf
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from funcs.conv import conv_jpx
from structs.res import AppRes
from widgets.toolbars import ToolBarMain
from widgets.charts import CandleStick, ChartNavigation


class StockExplorer(QMainWindow):
    __app_name__ = 'Stock Explorer'
    __version__ = '0.4.0'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1200, 700)

        # ツールバー
        toolbar = ToolBarMain(self.res)
        toolbar.enteredSymbol.connect(self.on_select_symbol)
        self.addToolBar(toolbar)

        # プロット用キャンバス
        self.canvas = canvas = CandleStick(res)
        self.setCentralWidget(canvas)

        # ツールバー（チャートのナビゲーション用）
        navtoolbar = ChartNavigation(canvas)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navtoolbar)

    def on_select_symbol(self, symbol: str):
        # 東証の銘柄コードであれば末尾に .T を付加する
        symbol = conv_jpx(symbol)
        ticker = yf.Ticker(symbol)
        self.canvas.plot(ticker)


def main():
    app = QApplication(sys.argv)
    win = StockExplorer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
