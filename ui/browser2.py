from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QStatusBar

from snippets.web_login import get_login_info
from ui.toolbar_traiding import ToolBarTrading
from ui.win_html import WinHTML


class BrowserTraiding(QMainWindow):
    def __init__(self, url_init: QUrl):
        super().__init__()
        self.url_init = url_init
        self.toolbar = None
        self.statusbar = None
        self.view = None
        self.win_html = None

        self.toolbar = toolbar = ToolBarTrading()
        toolbar.Back.connect(self.back)
        toolbar.Forward.connect(self.forward)
        toolbar.Load.connect(self.load)
        toolbar.Source.connect(self.source_requested)
        self.addToolBar(toolbar)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.view = view = QWebEngineView()
        view.loadFinished.connect(self.load_finished)
        self.setCentralWidget(view)

        toolbar.setURL(url_init)
        view.load(url_init)

        page: QWebEnginePage = view.page()
        page.titleChanged.connect(self.setWindowTitle)
        page.urlChanged.connect(self.url_changed)

        self.resize(1300, 1000)

    def load(self, url_str: str):
        url = QUrl.fromUserInput(url_str)
        if url.isValid():
            self.view.load(url)

    def load_finished(self, flag: bool):
        print('finished loading!', flag)
        if self.url_init == self.view.url().toString():
            self.page_login()

    def back(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Back)

    def forward(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Forward)

    def page_login(self):
        print('Login Page')
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
        page: QWebEnginePage = self.view.page()
        page.runJavaScript(jscript)

    def print_html(self, content):
        # print(content)
        self.win_html = win_html = WinHTML(content)
        win_html.show()

    def source_requested(self):
        page = self.view.page()
        # page.runJavaScript(self.jscript, 0, self.auxiliary)
        page.runJavaScript(
            'document.documentElement.outerHTML',
            0, self.print_html
        )

    def url_changed(self, url: QUrl):
        self.toolbar.setURL(url)
