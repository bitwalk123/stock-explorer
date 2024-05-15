#!/usr/bin/env python
# coding: utf-8
import re
import sys

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

from snippets.web_login import get_login_info


class Example(QWebEngineView):
    url_login = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')

    def __init__(self):
        super().__init__()
        self.content_prev = ''
        self.pattern_price = re.compile('([0-9,]+)（([0-9]{1,2}:[0-9]{2}:[0-9]{2})）')

        self.obj_login = get_login_info()
        self.load(self.url_login)
        self.loadFinished.connect(self.on_load_finished)
        page: QWebEnginePage = self.page()
        page.titleChanged.connect(self.setWindowTitle)
        self.resize(1300, 800)

    def on_load_finished(self, flag: bool) -> bool:
        if not flag:
            return False
        # self.page().toHtml(self.print_html)
        page: QWebEnginePage = self.page()
        title = page.title()
        if title == '総合口座ログイン | 楽天証券':
            self.op_login()
        elif title == 'ホーム | 楽天証券[PC]':
            self.op_domestic()
        elif title == '国内株式トップ | 株価検索 | 国内株式トップ | 国内株式 | 楽天証券[PC]':
            self.op_search()
            self.timer_start()
        elif title == '東京エレクトロン-株価 | 株価検索 | 国内株式トップ | 国内株式 | 楽天証券[PC]':
            self.op_price()
        else:
            print(title)
        return True

    def op_domestic(self):
        jscript = """
            var element1 = document.getElementById('gmenu_domestic_stock');
            var element2 = element1.getElementsByClassName('pcm-gl-nav-01__button')[0];
            element2.onclick.apply();
        """
        self.run_javascript(jscript)

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
        self.run_javascript(jscript)

    def op_price(self):
        jscript = """
            var element1 = document.getElementById('update_table0');
            var element2 = element1.getElementsByClassName('tbl-stock-price')[0];
            var element_price = element1.getElementsByClassName('price-01')[0];
            var element_time = element1.getElementsByClassName('time-01')[0];
            var str_price = element_price.textContent.trim();
            var str_time = element_time.textContent.trim();
            str_price + str_time;
        """
        self.run_javascript_2(jscript)

    def op_search(self):
        ticker = '8035'
        jscript = """
            var input_ticker_name = document.getElementById('dscrCdNm2');
            input_ticker_name.value = '%s';
            var element1 = document.getElementsByClassName('btn-box')[0];
            var element2 = element1.getElementsByClassName('roll')[0];
            element2.onclick.apply();
        """ % ticker
        self.run_javascript(jscript)

    def print_content(self, content: str):
        if content == self.content_prev:
            return

        self.content_prev = content
        m = self.pattern_price.match(content)
        if not m:
            return

        price_value = m.group(1)
        price_time = m.group(2)
        print(price_value, price_time)

    def run_javascript(self, jscript):
        page: QWebEnginePage = self.page()
        page.runJavaScript(jscript)

    def run_javascript_2(self, jscript):
        page: QWebEnginePage = self.page()
        page.runJavaScript(jscript, 0, self.print_content)

    def timer_start(self):
        timer = QTimer(self)
        timer.timeout.connect(self.reload)
        timer.start(10000)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
