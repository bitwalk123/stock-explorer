import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QWidget, QVBoxLayout,
)

from snippets.web_login import get_login_info
from ui.browser2 import BrowserTraiding


class TradingConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        self.obj_login = get_login_info()

        self.statusbar = None
        self.browser = None

        self.init_ui()
        self.show_browser()

        self.setWindowTitle('Trading Console')

    def init_ui(self):
        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout()
        base.setLayout(layout)

        but_login = QPushButton('Login')
        layout.addWidget(but_login)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    def show_browser(self):
        self.browser = BrowserTraiding(self.obj_login.getURL())
        self.browser.show()


def main():
    app = QApplication(sys.argv)
    win = TradingConsole()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
