import os
import sys
from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget, QHBoxLayout,
)

from snippets.web_login import get_login_info
from structs.res import AppRes
from ui.browser import BrowserTraiding
from widgets.buttons import TradingButton


class TradingConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        res = AppRes()
        self.obj_login = get_login_info()

        self.but_login = None
        self.but_domestic = None
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
        hbox_row2 = QHBoxLayout()
        layout.addLayout(hbox_row2)

        self.but_domestic = but_domestic = TradingButton('国内株式')
        but_domestic.setFunc('domestic')
        but_domestic.clicked.connect(self.op_domestic)
        hbox_row2.addWidget(but_domestic)

    def activate_login_button(self):
        self.but_login.setEnabled(True)
        self.but_domestic.setEnabled(True)

    def op_domestic(self):
        jscript = """
            var element = document.getElementById('gmenu_domestic_stock').getElementsByClassName('pcm-gl-nav-01__button')[0];
            element.onclick.apply();
        """
        #self.browser.runJScriptDebug(jscript)
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

    def show_browser(self):
        self.browser = browser = BrowserTraiding(self.obj_login.getURL())
        browser.loginReady.connect(self.activate_login_button)
        browser.show()


def main():
    app = QApplication(sys.argv)
    win = TradingConsole()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
