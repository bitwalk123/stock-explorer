import sys
from typing import Union

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QWidget, QVBoxLayout,
)

from snippets.web_login import get_login_info
from ui.browser2 import BrowserTraiding
from widgets.buttons import TradingButton


class TradingConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        self.obj_login = get_login_info()

        self.statusbar = None
        self.browser: Union[BrowserTraiding, None] = None

        self.init_ui()
        self.show_browser()

        self.setWindowTitle('Trading Console')

    def init_ui(self):
        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout()
        base.setLayout(layout)

        but_login = TradingButton('ログイン')
        but_login.setFunc('login')
        but_login.clicked.connect(self.op_login)
        layout.addWidget(but_login)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    def activate_buttons(self):
        print('Login ready')

    def op_login(self):
        obj_login = get_login_info()
        loginid = obj_login.getLoginID()
        password = obj_login.getPassword()
        jscript = """
            var input_username = document.getElementById('form-login-id');
            input_username.value = '%s';
            var input_username = document.getElementById('form-login-pass');
            input_username.value = '%s';
            //var button = document.getElementById('login-btn');
            //button.click();
        """ % (loginid, password)
        self.browser.runJScript(jscript)

    def show_browser(self):
        self.browser = browser = BrowserTraiding(self.obj_login.getURL())
        browser.loginReady.connect(self.activate_buttons)
        browser.show()


def main():
    app = QApplication(sys.argv)
    win = TradingConsole()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
