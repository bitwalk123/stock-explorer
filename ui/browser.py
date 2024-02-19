import os

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QMainWindow, QStatusBar

from funcs.parser import parser_good_bad_1
from structs.res import AppRes
from ui.toolbar_browser import ToolBarBrowser
from ui.toolbar_traiding import ToolBarTrading
from widgets.view import BaseBrowserView


class Browser(QMainWindow):
    def __init__(self, url: QUrl, jscript: str):
        super().__init__()
        self.jscript = jscript
        self.toolbar = None
        self.statusbar = None
        self.view = None

        self.init_ui(url)
        self.resize(1000, 800)

    def init_ui(self, url_init: QUrl):
        self.toolbar = toolbar = ToolBarBrowser()
        toolbar.Back.connect(self.back)
        toolbar.Forward.connect(self.forward)
        toolbar.Load.connect(self.load)
        toolbar.Source.connect(self.source_requested)
        self.addToolBar(toolbar)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.view = view = BaseBrowserView()
        self.setCentralWidget(view)

        toolbar.setURL(url_init)
        view.load(url_init)
        page: QWebEnginePage = view.page()
        page.titleChanged.connect(self.setWindowTitle)
        page.urlChanged.connect(self.url_changed)

    def load(self, url_str: str):
        url = QUrl.fromUserInput(url_str)
        if url.isValid():
            self.view.load(url)

    def back(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Back)

    def forward(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Forward)

    def url_changed(self, url: QUrl):
        self.toolbar.setURL(url)

    def auxiliary(self, content):
        print(content)

    def source_requested(self):
        page = self.view.page()
        page.runJavaScript(self.jscript, 0, self.auxiliary)


class NewsGoodBad(Browser):
    # codeSelected = Signal(str)
    goodbadRequested = Signal(dict)

    def __init__(self, url: QUrl, jscript: str):
        super().__init__(url, jscript)
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'kabutan.png'))
        self.setWindowIcon(icon)

    def auxiliary(self, content):
        dict_df = parser_good_bad_1(content)
        self.goodbadRequested.emit(dict_df)


class RakutenRanking(Browser):
    parseRequested = Signal(str)

    def __init__(self, url: QUrl, jscript: str):
        super().__init__(url, jscript)
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'rakuten.png'))
        self.setWindowIcon(icon)

    def auxiliary(self, content):
        # print(content)
        # print(type(content))
        self.parseRequested.emit(content)


class BrowserTraiding(QMainWindow):
    loginReady = Signal()

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
        self.addToolBar(toolbar)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.view = view = BaseBrowserView()
        view.loadFinished.connect(self.load_finished)
        self.setCentralWidget(view)

        toolbar.setURL(url_init)
        view.load(url_init)

        page: QWebEnginePage = view.page()
        page.titleChanged.connect(self.setWindowTitle)
        page.urlChanged.connect(self.url_changed)

        self.resize(1300, 1000)

    def back(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Back)

    def forward(self):
        page: QWebEnginePage = self.view.page()
        page.triggerAction(QWebEnginePage.WebAction.Forward)

    def getPageTitle(self) -> str:
        page: QWebEnginePage = self.view.page()
        title = page.title()
        return title

    def load(self, url_str: str):
        url = QUrl.fromUserInput(url_str)
        if url.isValid():
            self.view.load(url)

    def load_finished(self, flag: bool):
        if self.url_init == self.view.url().toString():
            self.page_login()
        else:
            title = self.getPageTitle()
            print('finished loading page!', title)

    def page_login(self):
        print('Login Page')
        self.loginReady.emit()

    def runJScript(self, jscript: str):
        page: QWebEnginePage = self.view.page()
        page.runJavaScript(jscript)

    def url_changed(self, url: QUrl):
        self.toolbar.setURL(url)
