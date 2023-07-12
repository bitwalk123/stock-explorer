#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from functions.get_open_with_code import get_open_with_code
from functions.resources import get_ini_file
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain
from ui_modules.win_canvas import MplCanvas


class StockExplorer(QMainWindow):
    """Main class for this application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')

        self.plot = None

        # ini ファイル（フルパス）
        self.file_ini = get_ini_file()
        print(self.file_ini)

        # self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        # ツールバー
        toolbar = ToolBarMain()
        self.addToolBar(toolbar)
        # コードドック
        dock_left = DockTicker()
        dock_left.clicked.connect(self.on_ticker_selected)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)

        self.plot = MplCanvas()
        code = 5217
        self.draw_plot(code)
        self.setCentralWidget(self.plot)

    def draw_plot(self, code: int):
        """Draw plot with specified ticker code

        Args:
            code (int): ticker code
        """
        cname, list_x, list_y = get_open_with_code(code)
        self.plot.clearAxes()
        #
        self.plot.axes.plot(list_x, list_y)
        self.plot.axes.set_title('%s (%d.T)' % (cname, code))
        self.plot.axes.set_xlabel('日付')
        self.plot.axes.set_ylabel('株価')
        self.plot.axes.grid()
        #
        self.plot.refreshDraw()

    def on_ticker_selected(self, code):
        """Signal handler for ticker code button click

        Args:
            code (int): ticker code
        """
        print(code)
        self.draw_plot(code)

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
