import os
import sys
from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget, QHBoxLayout, QComboBox,
)

from snippets.web_login import get_login_info
from structs.res import AppRes
from structs.website import WebSite
from ui.browser import BrowserTraiding
from widgets.buttons import TradingButton


class TradingConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        res = AppRes()
        self.website = WebSite()
        self.obj_login = get_login_info()

        self.dict_ticker = {
            'ＳＣＲＥＥＮホールディングス (7735)': '7735',
        }

        self.but_login = None
        self.but_domestic = None
        self.combo_ticker: Union[QComboBox, None] = None
        self.but_search = None
        self.statusbar = None
        self.init_ui()

        self.browser: Union[BrowserTraiding, None] = None
        self.show_browser()

        self.setWindowTitle('Trading Console')
        icon = QIcon(os.path.join(res.getImagePath(), 'rakuten.png'))
        self.setWindowIcon(icon)

    def closeEvent(self, event):
        if self.browser is not None:
            self.browser.hide()
            self.browser.deleteLater()
        event.accept()

    def init_ui(self):
        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout()
        base.setLayout(layout)

        # Row 1
        self.but_login = but_login = TradingButton('ログイン')
        but_login.setFunc('login')
        but_login.clicked.connect(self.op_login)
        layout.addWidget(but_login)

        # Row 2
        self.but_domestic = but_domestic = TradingButton('国内株式')
        but_domestic.setFunc('domestic')
        but_domestic.clicked.connect(self.op_domestic)
        layout.addWidget(but_domestic)

        # Row 3
        box_row3 = QHBoxLayout()
        layout.addLayout(box_row3)

        self.combo_ticker = combo_ticker = QComboBox()
        combo_ticker.setFixedWidth(300)
        combo_ticker.addItems(self.dict_ticker.keys())
        box_row3.addWidget(combo_ticker)

        self.but_search = but_search = TradingButton('検索')
        but_search.setFunc('search')
        but_search.clicked.connect(self.op_search)
        box_row3.addWidget(but_search)

    def activate_login_button(self):
        self.but_login.setEnabled(True)

    def activate_domestic(self):
        self.but_domestic.setEnabled(True)

    def activate_search(self):
        self.but_search.setEnabled(True)

    def deactivate_login_button(self):
        self.but_login.setEnabled(False)

    def load_finished(self, title: str):
        print('finished loading page!', title)
        if self.website.checkSite(title, 'home'):
            self.deactivate_login_button()
            self.activate_domestic()
        elif self.website.checkSite(title, 'domestic'):
            self.activate_search()

    def op_domestic(self):
        jscript = """
            var element = document.getElementById('gmenu_domestic_stock').getElementsByClassName('pcm-gl-nav-01__button')[0];
            element.onclick.apply();
        """
        self.browser.runJScript(jscript)

    def op_login(self):
        obj_login = get_login_info()
        loginid = obj_login.getLoginID()
        password = obj_login.getPassword()
        jscript = """
            var input_username = document.getElementById('form-login-id');
            input_username.value = '%s';
            var input_username = document.getElementById('form-login-pass');
            input_username.value = '%s';
            var button = document.getElementById('login-btn');
            button.click();
        """ % (loginid, password)
        self.browser.runJScript(jscript)

    def op_search(self):
        name_ticker = self.combo_ticker.currentText()
        ticker = self.dict_ticker[name_ticker]
        print(ticker)

    def show_browser(self):
        self.browser = browser = BrowserTraiding(self.obj_login.getURL())
        browser.loginReady.connect(self.activate_login_button)
        browser.loadFinished.connect(self.load_finished)
        browser.show()


def main():
    app = QApplication(sys.argv)
    win = TradingConsole()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
