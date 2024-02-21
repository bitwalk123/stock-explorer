from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineDownloadRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFileDialog

from ui.win_html import WinHTML


class BaseBrowserView(QWebEngineView):
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
            self, 'Save File', url_path, '*.' + suffix
        )
        if path:
            download.setDownloadFileName(path)
            download.accept()

    def print_html(self, content):
        self.win_html = win_html = WinHTML(content)
        win_html.show()
