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

"""
print(driver.title)
"""


class Trader(QMainWindow):
    url_login = 'https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html'

    def __init__(self):
        super().__init__()
        res = AppRes()
        self.obj_login = get_login_info()

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
        name_id = 'form-login-pass'
        if self.show_url(driver, self.url_login, name_id):
            self.activate_login_button()

    def activate_login_button(self):
        self.but_login.setEnabled(True)

    def op_login(self):
        loginid = self.obj_login.getLoginID()
        password = self.obj_login.getPassword()

    def show_url(self, driver: webdriver.Chrome | webdriver.Firefox, url: str, name_id: str) -> bool:
        driver.get(url)
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


def main():
    app = QApplication(sys.argv)
    win = Trader()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
