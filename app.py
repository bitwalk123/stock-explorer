#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from functions.draw_trend import draw_trend
from functions.resources import get_ini_file
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain
from ui_modules.charts import Trend


class StockExplorer(QMainWindow):
    """Main class for this application
    """

    def __init__(self):
        super().__init__()
        self.chart = None

        # ini ファイル（フルパス）
        self.file_ini = get_ini_file()
        print(self.file_ini)

        self.setWindowTitle('Stock Explorer')
        # self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        # ツールバー
        toolbar = ToolBarMain()
        self.addToolBar(toolbar)
        # コードドック
        dock_left = DockTicker()
        dock_left.clicked.connect(self.on_ticker_selected)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)

        self.chart = Trend()
        code = 5217
        draw_trend(self.chart, code)
        self.setCentralWidget(self.chart)

    def on_ticker_selected(self, code):
        """Signal handler for ticker code button click

        Args:
            code (int): ticker code
        """
        print(code)
        draw_trend(code)

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        print('アプリケーションを終了します。')
        event.accept()  # let the window close


def main():
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
