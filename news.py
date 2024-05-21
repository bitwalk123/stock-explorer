import sys

from PySide6.QtCore import QCoreApplication, Signal, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QPushButton,
    QToolBar, QScrollArea, QWidget, QGridLayout, QLabel,
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
        self.resize(600, 300)

        toolbar = ToolBarNews()
        toolbar.clickedSearch.connect(self.on_search)
        self.addToolBar(toolbar)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        self.setCentralWidget(sa)

        self.base = base = QWidget()
        sa.setWidget(base)

        self.layout = QGridLayout()
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.base.setLayout(self.layout)

    def new_layout(self):
        for r in range(self.layout.rowCount()):
            for c in range(self.layout.columnCount()):
                item = self.layout.itemAtPosition(r, c)
                if item is not None:
                    item.widget().deleteLater()
                    self.layout.removeItem(item)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def on_search(self, ticker: str):
        self.new_layout()
        r = 0

        # _____________________________________________________________________
        # 株予想
        results = get_news_kabuyoho(ticker)
        for line in results:
            lab_date = QLabel(line[0])
            self.layout.addWidget(lab_date, r, 0)

            msg = line[1]
            url = line[2]
            lab_news = QLabel()
            lab_news.setText('<a href="%s">%s</a>' % (url, msg))
            lab_news.setOpenExternalLinks(True)
            self.layout.addWidget(lab_news, r, 1)

            r += 1

    def on_exit(self):
        QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    win = News()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
