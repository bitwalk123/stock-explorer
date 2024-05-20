import sys

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QMainWindow):
    kabuyoho = 'https://kabuyoho.ifis.co.jp/index.php?action=tp1&sa=report_top&bcode=%s'

    def __init__(self):
        super().__init__()
        self.browser = None
        self.tickers = tickers = {'東京エレクトロン': '8035', }
        self.setWindowTitle('News')

        base = QWidget()
        self.setCentralWidget(base)

        vbox = QVBoxLayout()
        vbox.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        base.setLayout(vbox)

        row_1 = QHBoxLayout()

        self.combo = combo = QComboBox()
        combo.addItems(tickers.keys())
        combo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        row_1.addWidget(combo)

        but_search = QPushButton('検索')
        but_search.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred
        )
        but_search.clicked.connect(self.on_search)
        row_1.addWidget(but_search)

        vbox.addLayout(row_1)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        if type(self.browser) is not None:
            self.browser.close()
        event.accept()  # let the window close

    def on_load_finished(self, flag: bool) -> bool:
        page: QWebEnginePage = self.browser.page()
        title = page.title()
        print(title)
        self.run_javascript()

        return True

    def on_search(self):
        key = self.combo.currentText()
        ticker = self.tickers[key]
        url = self.kabuyoho % ticker
        print(url)

        self.browser = QWebEngineView()
        self.browser.loadFinished.connect(self.on_load_finished)
        self.browser.load(url)
        self.browser.show()

    def print_content(self, content: str):
        print(content)

    def run_javascript(self):
        page: QWebEnginePage = self.browser.page()
        page.runJavaScript('document.documentElement.outerHTML;', 0, self.print_content)

    def on_exit(self):
        QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
