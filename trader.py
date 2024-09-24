import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from snippets.web_login import get_login_info
from structs.res import AppRes
from widgets.buttons import TradingButton


class Trader(QMainWindow):
    url_login = 'https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html'
    dict_id = {
        'login': 'form-login-id',  # ログイン・アカウント
        'passwd': 'form-login-pass',  # ログイン・パスワード
        'login-button': 'login-btn',  # ログイン・ボタン
    }

    def __init__(self):
        super().__init__()
        res = AppRes()

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Main panel
        base = QWidget()
        self.setCentralWidget(base)
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        base.setLayout(layout)

        # Login
        self.but_login = but_login = TradingButton('ログイン')
        but_login.setFunc('login')
        but_login.clicked.connect(self.op_login)
        layout.addWidget(but_login)

        # Logout
        self.but_logout = but_logout = TradingButton('ログアウト')
        but_logout.setFunc('logout')
        but_logout.clicked.connect(self.op_logout)
        layout.addWidget(but_logout)

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Frame decoration
        self.setStyleSheet("""
            QMainWindow{background-color: #321;}
        """)
        self.setWindowTitle('Trader')
        icon = QIcon(os.path.join(res.getImagePath(), 'rakuten.png'))
        self.setWindowIcon(icon)
        # self.setFixedSize(self.sizeHint())

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # Browser initialization
        self.driver = driver = webdriver.Firefox()
        self.show_url_login()

    def change_status_login_button(self, status: bool = True):
        self.but_login.setEnabled(status)

    def op_login(self):
        obj_login = get_login_info()

        entry_login = self.driver.find_element('id', self.dict_id['login'])
        entry_login.clear()
        entry_login.send_keys(obj_login.getLoginID())

        entry_passwd = self.driver.find_element('id', self.dict_id['passwd'])
        entry_passwd.clear()
        entry_passwd.send_keys(obj_login.getPassword())

        button_login = self.driver.find_element('id', self.dict_id['login-button'])
        button_login.submit()

    def op_logout(self):
        pass

    def show_url(self, driver: webdriver.Chrome | webdriver.Firefox, name_id: str) -> bool:
        delay = 5  # seconds

        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located(
                    (By.ID, name_id)
                )
            )
            print('Page is ready!')
            return True
        except TimeoutException:
            print('Loading took too much time!')
            return False

    def show_url_login(self):
        self.driver.get(self.url_login)
        if self.show_url(self.driver, self.dict_id['passwd']):
            self.change_status_login_button()


def main():
    app = QApplication(sys.argv)
    win = Trader()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
