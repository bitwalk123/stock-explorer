from PySide6.QtCore import (
    QFileInfo,
    QUrl,
    Signal,
)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
    QWebEnginePage,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QStatusBar,
)

from ui.toolbar_traiding import ToolBarTrading
from ui.win_html import WinHTML


class TradingView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.win_html = None
        self.page().profile().downloadRequested.connect(
            self.on_download_requested
        )

    def createWindow(self, wwtype: QWebEnginePage.WebWindowType):
        action: QAction = self.pageAction(QWebEnginePage.WebAction.ViewSource)
        if action.isEnabled():
            self.page().toHtml(self.print_html)

    def on_download_requested(self, download: QWebEngineDownloadRequest):
        url_path = download.url().path()  # download.path()
        if url_path == '/':
            url_path = 'index.html'
        suffix = QFileInfo(url_path).suffix()
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", url_path, "*." + suffix
        )
        if path:
            download.setDownloadDirectory(path)
            download.accept()

    def print_html(self, content):
        self.win_html = win_html = WinHTML(content)
        win_html.show()


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
        # toolbar.Source.connect(self.source_requested)
        self.addToolBar(toolbar)

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # self.view = view = QWebEngineView()
        self.view = view = TradingView()
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
