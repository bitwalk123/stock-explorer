import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from snippets.web_login import get_login_info


class TradeDayAnalysisProto(QMainWindow):
    url_login = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')

    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.obj_login = get_login_info()
        self.browser.load(self.url_login)
        self.browser.loadFinished.connect(self.on_load_finished)

        # _____________________________________________________________________
        self.resize(1350, 800)

    def on_load_finished(self, flag: bool) -> bool:
        if not flag:
            return False

        page: QWebEnginePage = self.browser.page()
        title = page.title()
        if title == '総合口座ログイン | 楽天証券':
            self.op_login()
        elif title == 'ホーム | 楽天証券[PC]':
            self.op_domestic()
        else:
            print(title)
        return True

    def op_domestic(self):
        jscript1 = """
            $.cookie(autoLogoutStsCookieKey, "0");
            autoLogout = false;
            autoLogoutUsed = true;
        """
        self.run_javascript(jscript1)

        jscript2 = """
            var element1 = document.getElementById('gmenu_domestic_stock');
            var element2 = element1.getElementsByClassName('pcm-gl-nav-01__button')[0];
            element2.onclick.apply();
        """
        self.run_javascript(jscript2)

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

    def run_javascript(self, jscript):
        page: QWebEnginePage = self.browser.page()
        page.runJavaScript(jscript)

    def run_javascript_2(self, jscript):
        page: QWebEnginePage = self.browser.page()
        page.runJavaScript(jscript, 0, self.print_content)

    def print_content(self, content: str):
        print(content)


def main():
    app = QApplication()
    ex = TradeDayAnalysisProto()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
