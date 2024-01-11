import os
import sys

from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QTabWidget,
)

from snippets.set_env import set_env
from structs.res import AppRes
from ui.main_domestic import MainDomesticStocks
from ui.main_exchange import MainExchange


class StockExplorer(QTabWidget):
    __version__ = '0.2.0'
    __build__ = '20240111'

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabPosition(QTabWidget.TabPosition.West)

        font = QFontDatabase.systemFont(
            QFontDatabase.SystemFont.FixedFont
        )
        self.setFont(font)

        dict_info = set_env()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'stock.png'))
        self.setWindowIcon(icon)

        self.init_ui()
        self.setWindowTitle('Stock Explorer - %s' % self.__version__)
        self.resize(1200, 700)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def init_ui(self):
        list_content = [
            MainDomesticStocks(self),
            MainExchange(self),
        ]
        for content in list_content:
            self.addTab(content, content.getTabLabel())


def main():
    app = QApplication(sys.argv)
    win = StockExplorer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
