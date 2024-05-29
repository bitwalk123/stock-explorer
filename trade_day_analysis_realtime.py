#!/usr/bin/env python
# coding: utf-8
import datetime
import os
import pandas as pd
import re
import sys

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from funcs.tide import get_timestamp
from snippets.web_login import get_login_info
from widgets.charts import ChartRealtime


class Example(QTabWidget):
    url_login = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')

    def __init__(self):
        super().__init__()
        self.ticker = '8035'
        self.content_prev = ''
        self.pattern_price = re.compile('([0-9,]+)（([0-9]{1,2}:[0-9]{2}:[0-9]{2})）')
        self.time_open = pd.to_datetime('08:59:00')
        self.time_close = pd.to_datetime('15:01:00')
        self.time_lunch_1 = pd.to_datetime('11:31:00')
        self.time_lunch_2 = pd.to_datetime('12:29:00')
        self.df = pd.DataFrame()
        self.timer = QTimer(self)

        # _____________________________________________________________________
        tab1 = QMainWindow()
        self.addTab(tab1, 'Browser')

        self.browser = QWebEngineView()
        tab1.setCentralWidget(self.browser)

        self.obj_login = get_login_info()
        self.browser.load(self.url_login)
        self.browser.loadFinished.connect(self.on_load_finished)

        page: QWebEnginePage = self.browser.page()
        page.titleChanged.connect(self.setWindowTitle)

        # _____________________________________________________________________
        tab2 = QMainWindow()
        self.addTab(tab2, 'Chart')
        self.chart = chart = ChartRealtime()
        tab2.setCentralWidget(chart)

        dt = datetime.datetime.today()
        date_str= '%4d-%02d-%02d' % (dt.year, dt.month, dt.day)
        self.time_left = pd.to_datetime(date_str + ' 08:50:00')
        self.time_mid = pd.to_datetime(date_str + ' 12:00:00')
        self.time_right = pd.to_datetime(date_str + ' 15:10:00')
        self.chart.ax.set_xlim(self.time_left, self.time_right)

        # _____________________________________________________________________
        self.resize(1300, 800)

    def get_pkl_fine(self) -> str:
        return 'tmp/%s_%s.pkl' % (self.ticker, str(get_timestamp().date()))

    def on_load_finished(self, flag: bool) -> bool:
        if not flag:
            return False
        # self.page().toHtml(self.print_html)
        page: QWebEnginePage = self.browser.page()
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
        jscript = """
            var input_ticker_name = document.getElementById('dscrCdNm2');
            input_ticker_name.value = '%s';
            var element1 = document.getElementsByClassName('btn-box')[0];
            var element2 = element1.getElementsByClassName('roll')[0];
            element2.onclick.apply();
        """ % self.ticker
        self.run_javascript(jscript)

    def print_content(self, content: str):
        ts = get_timestamp()
        if ts < self.time_open:
            # print('before market open')
            return

        if content == self.content_prev:
            return

        self.content_prev = content
        m = self.pattern_price.match(content)
        if not m:
            print('*** no match ***')
            return

        str1 = m.group(1)
        str2 = m.group(2)

        # Convert appropriate types
        price_value = float(str1.replace(',', ''))
        price_time = pd.to_datetime(str2)

        if len(self.df) == 0:
            # 最初のみデータフレームを（再）生成
            self.df = pd.DataFrame(
                {'Price': [price_value]},
                index=[price_time]
            )
        else:
            # データの追加
            self.df.loc[price_time] = price_value

        print(price_time, price_value)

        # _____________________________________________________________________
        # Chart
        self.chart.clearAxes()
        df1 = self.df.loc[self.df.index[self.df.index < self.time_mid]]
        df2 = self.df.loc[self.df.index[self.df.index > self.time_mid]]
        if len(df1) > 0:
            self.chart.ax.plot(df1, c='C0')
        if len(df2) > 0:
            self.chart.ax.plot(df2, c='C0')
        self.chart.ax.set_xlim(self.time_left, self.time_right)
        self.chart.ax.grid()
        self.chart.refreshDraw()

    def run_javascript(self, jscript):
        page: QWebEnginePage = self.browser.page()
        page.runJavaScript(jscript)

    def run_javascript_2(self, jscript):
        page: QWebEnginePage = self.browser.page()
        page.runJavaScript(jscript, 0, self.print_content)

    def timer_start(self):
        self.timer.timeout.connect(self.web_reload)
        self.timer.start(10000)
        print('timer started')

    def web_reload(self):
        ts = get_timestamp()
        if ts < self.time_open:
            # print('before market open')
            return

        if (ts > self.time_lunch_1) and (ts < self.time_lunch_2):
            # print('lunch break')
            return

        if ts > self.time_close:
            # print('after market close')
            pkl = self.get_pkl_fine()
            if not os.path.exists(pkl):
                self.df.to_pickle(pkl)
                print('saved %s' % pkl)
                self.timer.stop()
                print('timer stopped')

            return
        # RELOAD
        self.browser.reload()


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
