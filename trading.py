import os
import sys
from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget, QLineEdit, QPushButton,
)

from snippets.web_login import get_login_info
from structs.res import AppRes
from structs.website import WebSite
from ui.browser import BrowserTraiding
from widgets.buttons import TradingButton, LockButton
from widgets.entries import SpinBox


class TradingConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        res = AppRes()
        self.setStyleSheet("""
            QMainWindow{background-color: #321;}
        """)

        self.website = WebSite()
        self.obj_login = get_login_info()

        self.dict_ticker = {
            'ＳＣＲＥＥＮホールディングス': '7735',
            '東京エレクトロン': '8035',
            'アドバンテスト': '6857',
        }

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Main panel
        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
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

        self.but_lock_ticker = but_lock_ticker = LockButton()
        box_row3.addWidget(but_lock_ticker)

        self.combo_ticker = combo_ticker = QComboBox()
        combo_ticker.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        combo_ticker.setMinimumWidth(250)
        combo_ticker.addItems(self.dict_ticker.keys())
        box_row3.addWidget(combo_ticker)

        self.but_search = but_search = TradingButton('検索')
        but_search.setFunc('search')
        but_search.clicked.connect(self.op_search)
        box_row3.addWidget(but_search)

        # Row 4
        box_row4 = QGridLayout()
        box_row4.setColumnStretch(0, 1)
        box_row4.setColumnStretch(2, 1)
        box_row4.setColumnStretch(4, 1)
        box_row4.setContentsMargins(0, 0, 0, 0)
        box_row4.setSpacing(2)
        layout.addLayout(box_row4)

        self.but_buynew = but_buynew = TradingButton('信用新規')
        but_buynew.setFunc('buynew')
        but_buynew.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        but_buynew.clicked.connect(self.op_buynew)
        box_row4.addWidget(but_buynew, 0, 0, 2, 1)

        self.but_lock_long = but_lock_long = LockButton()
        box_row4.addWidget(but_lock_long, 0, 1)

        self.spin_long = spin_long = SpinBox()
        box_row4.addWidget(spin_long, 0, 2)

        self.but_long = but_long = TradingButton('買　建')
        but_long.setFunc('long')
        but_long.clicked.connect(self.op_long)
        box_row4.addWidget(but_long, 1, 1, 1, 2)

        self.but_lock_short = but_lock_short = LockButton()
        box_row4.addWidget(but_lock_short, 0, 3)

        self.spin_short = spin_short = SpinBox()
        box_row4.addWidget(spin_short, 0, 4)

        self.but_short = but_short = TradingButton('売　建')
        but_short.setFunc('short')
        but_short.clicked.connect(self.op_short)
        box_row4.addWidget(but_short, 1, 3, 1, 2)

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Status bar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.lab_msg = lab_msg = QLineEdit()
        lab_msg.setEnabled(False)
        statusbar.addPermanentWidget(lab_msg, stretch=1)

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Browser
        self.browser: Union[BrowserTraiding, None] = None
        self.show_browser()

        # Console window
        self.setWindowTitle('Trading Console')
        icon_lock = QIcon(os.path.join(res.getImagePath(), 'rakuten.png'))
        self.setWindowIcon(icon_lock)

        self.setFixedSize(self.sizeHint())

    def activate_buynew(self):
        self.but_buynew.setEnabled(True)

    def activate_login_button(self):
        self.but_login.setEnabled(True)

    def activate_long(self):
        self.but_long.setEnabled(True)

    def activate_domestic(self):
        self.but_domestic.setEnabled(True)

    def activate_search(self):
        self.but_search.setEnabled(True)

    def activate_short(self):
        self.but_short.setEnabled(True)

    def closeEvent(self, event):
        if self.browser is not None:
            self.browser.hide()
            self.browser.deleteLater()
        event.accept()

    def deactivate_buynew(self):
        self.but_buynew.setEnabled(False)

    def deactivate_long(self):
        self.but_long.setEnabled(False)

    def deactivate_login_button(self):
        self.but_login.setEnabled(False)

    def deactivate_search(self):
        self.but_search.setEnabled(False)

    def deactivate_short(self):
        self.but_short.setEnabled(False)

    def load_finished(self, title: str):
        print('finished loading page!', title)
        if self.website.checkSite(title, 'home'):
            self.deactivate_login_button()
            self.activate_domestic()
            self.deactivate_search()
            self.deactivate_buynew()
            self.deactivate_long()
            self.deactivate_short()
        elif self.website.checkSite(title, 'domestic'):
            self.activate_search()
            self.deactivate_buynew()
            self.deactivate_long()
            self.deactivate_short()
        elif self.website.checkSite(title, 'ticker', self.combo_ticker.currentText()):
            self.deactivate_search()
            self.activate_buynew()
            self.deactivate_long()
            self.deactivate_short()
        elif self.website.checkSite(title, 'buynew'):
            self.deactivate_buynew()
            self.activate_long()
            self.activate_short()

    def op_buynew(self):
        jscript = """
            var element1 = document.getElementById('linkBuyNew');
            var element2 = element1.getElementsByClassName('pcmm_jpstk-btlk-margin-open pcmm_jpstk-btlk-filled pcmm_jpstk-btlk--xs pcmm_jpstk-btlk--block')[0];
            element2.click();
        """
        self.browser.runJScript(jscript)

    def op_domestic(self):
        jscript = """
            var element1 = document.getElementById('gmenu_domestic_stock');
            var element2 = element1.getElementsByClassName('pcm-gl-nav-01__button')[0];
            element2.onclick.apply();
        """
        self.browser.runJScript(jscript)

    def op_login(self):
        loginid = self.obj_login.getLoginID()
        password = self.obj_login.getPassword()
        jscript = """
            var input_username = document.getElementById('form-login-id');
            input_username.value = '%s';
            var input_username = document.getElementById('form-login-pass');
            input_username.value = '%s';
            var button = document.getElementById('login-btn');
            button.click();
        """ % (loginid, password)
        self.browser.runJScript(jscript)

    def op_long(self):
        deltavalue = 50
        passnumber = self.obj_login.getPassnumber()
        jscript = """
            var tradetype = document.getElementById('buy');
            tradetype.checked = true;
            tradetype.onclick.apply();

            var maturity = document.getElementById('general_1d');
            maturity.checked = true;
            maturity.onclick.apply();

            var ordervalue = document.getElementById('orderValue');
            ordervalue.value = 100;

            // 成行
            var marketorderkbn = document.getElementById('priceMarket');
            marketorderkbn.checked = true;
            marketorderkbn.onclick.apply();

            var dosetorder = document.getElementById('doSetOrder');
            dosetorder.checked = true;
            dosetorder.onclick.apply();

            var setorderpricekbn = document.getElementById('profitMargin');
            setorderpricekbn.checked = true;
            setorderpricekbn.onclick.apply();

            var setorderpricekbn2 = document.getElementById('profitMarginPrice');
            setorderpricekbn2.value = %d;
            
            var password = document.getElementsByName('password')[0];
            password.value = '%s';
        """ % (deltavalue, passnumber)
        self.browser.runJScript(jscript)

    def op_short(self):
        deltavalue = 25
        passnumber = self.obj_login.getPassnumber()
        jscript = """
            var tradetype = document.getElementById('sell');
            tradetype.checked = true;
            tradetype.onclick.apply();

            var maturity = document.getElementById('general_1d');
            maturity.checked = true;
            maturity.onclick.apply();

            var ordervalue = document.getElementById('orderValue');
            ordervalue.value = 100;

            // 成行
            var marketorderkbn = document.getElementById('priceMarket');
            marketorderkbn.checked = true;
            marketorderkbn.onclick.apply();

            var dosetorder = document.getElementById('doSetOrder');
            dosetorder.checked = true;
            dosetorder.onclick.apply();

            var setorderpricekbn = document.getElementById('profitMargin');
            setorderpricekbn.checked = true;
            setorderpricekbn.onclick.apply();

            var setorderpricekbn2 = document.getElementById('profitMarginPrice');
            setorderpricekbn2.value = %d;

            var password = document.getElementsByName('password')[0];
            password.value = '%s';
        """ % (deltavalue, passnumber)
        self.browser.runJScript(jscript)

    def op_search(self):
        name_ticker = self.combo_ticker.currentText()
        ticker = self.dict_ticker[name_ticker]
        jscript = """
            var input_ticker_name = document.getElementById('dscrCdNm2');
            input_ticker_name.value = '%s';
            var element1 = document.getElementsByClassName('btn-box')[0];
            var element2 = element1.getElementsByClassName('roll')[0];
            element2.onclick.apply();
        """ % ticker
        self.browser.runJScript(jscript)

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
