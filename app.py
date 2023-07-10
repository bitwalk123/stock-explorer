#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from functions.resources import get_ini_file
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain


class StockExplorer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')

        # ini ファイル（フルパス）
        self.file_ini = get_ini_file()
        print(self.file_ini)

        self.init_ui()

    def init_ui(self):
        # ツールバー
        toolbar = ToolBarMain()
        self.addToolBar(toolbar)
        dock_left = DockTicker()
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)


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
