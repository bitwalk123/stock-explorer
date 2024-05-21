import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QPushButton,
    QToolBar,
)

from funcs.scraping import get_news_kabuyoho


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tickers = tickers = {
            '東京エレクトロン': '8035',
            'ＳＣＲＥＥＮホールディングス': '7735',
            'アドバンテスト': '6857',
            'レーザーテック': '6920',
            'ディスコ': '6146',
        }
        self.setWindowTitle('News')

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.combo = combo = QComboBox()
        combo.addItems(tickers.keys())
        toolbar.addWidget(combo)

        but_search = QPushButton('検索')
        but_search.clicked.connect(self.on_search)
        toolbar.addWidget(but_search)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def on_search(self):
        key = self.combo.currentText()
        ticker = self.tickers[key]

        # 株予想
        results = get_news_kabuyoho(ticker)
        for line in results:
            print(line)

    def on_exit(self):
        QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
