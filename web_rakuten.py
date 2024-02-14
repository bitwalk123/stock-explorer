import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication

from ui.traiding import TradingBrowser


def main(url_init: QUrl):
    app = QApplication()
    ex = TradingBrowser(url_init)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')
    main(url)
