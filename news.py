import sys

from PySide6.QtCore import (
    QCoreApplication,
    Qt,
    Signal,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QToolBar,
    QWidget,
)

from funcs.scraping import get_news_kabuyoho, get_news_8035
from widgets.labels import (
    LabelLogo,
    LabelNewsDate,
    LabelNewsMsg,
)


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
            'アルバック': '6728',
            '信越化学': '4063',
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
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.base.setLayout(self.layout)

        self.browser = QWebEngineView()
        self.browser.page().titleChanged.connect(
            self.browser.setWindowTitle
        )

    def new_layout(self):
        for r in range(self.layout.rowCount()):
            for c in range(self.layout.columnCount()):
                item = self.layout.itemAtPosition(r, c)
                if item is not None:
                    item.widget().deleteLater()
                    self.layout.removeItem(item)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        self.browser.deleteLater()
        event.accept()  # let the window close

    def on_search(self, ticker: str):
        self.new_layout()
        r = 0

        # _____________________________________________________________________
        # 株予想
        results = get_news_kabuyoho(ticker)
        logo = 'images/kabuyoho.png'
        for line in results:
            lab_logo = LabelLogo(logo)
            self.layout.addWidget(lab_logo, r, 0)

            date = line[0]
            lab_date = LabelNewsDate(date)
            self.layout.addWidget(lab_date, r, 1)

            msg = line[1]
            url = line[2]
            lab_news = LabelNewsMsg(url, msg)
            lab_news.linkActivated.connect(self.show_url)
            self.layout.addWidget(lab_news, r, 2)

            r += 1

        # _____________________________________________________________________
        # 東京エレクトロン (8035)
        if ticker == '8035':
            results = get_news_8035()
            logo = 'images/8035.png'
            for line in results:
                lab_logo = LabelLogo(logo)
                self.layout.addWidget(lab_logo, r, 0)

                date = line[0]
                lab_date = LabelNewsDate(date)
                self.layout.addWidget(lab_date, r, 1)

                msg = line[1]
                url = line[2]
                lab_news = LabelNewsMsg(url, msg)
                lab_news.linkActivated.connect(self.show_url)
                self.layout.addWidget(lab_news, r, 2)

                r += 1

    def on_exit(self):
        QCoreApplication.quit()

    def show_url(self, url: str):
        self.browser.load(url)
        self.browser.show()


def main():
    app = QApplication(sys.argv)
    win = News()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
