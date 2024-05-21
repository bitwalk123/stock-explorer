import sys

from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QPushButton,
    QToolBar,
)

from funcs.scraping import get_news_kabuyoho


class ToolBarNews(QToolBar):
    clickedSearch = Signal(str)

    def __init__(self):
        super().__init__()

        self.tickers = {
            '東京エレクトロン': '8035',
            'ＳＣＲＥＥＮホールディングス': '7735',
            'アドバンテスト': '6857',
            'レーザーテック': '6920',
            'ディスコ': '6146',
        }

        self.combo = combo = QComboBox()
        combo.addItems(self.tickers.keys())
        self.addWidget(combo)

        but_search = QPushButton('検索')
        but_search.clicked.connect(self.on_search)
        self.addWidget(but_search)

    def on_search(self):
        key = self.combo.currentText()
        ticker = self.tickers[key]
        self.clickedSearch.emit(ticker)


class News(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('News')

        toolbar = ToolBarNews()
        toolbar.clickedSearch.connect(self.on_search)
        self.addToolBar(toolbar)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def on_search(self, ticker: str):
        # 株予想
        results = get_news_kabuyoho(ticker)
        for line in results:
            print(line)

    def on_exit(self):
        QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    win = News()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
