#!/usr/bin/env python
# coding: utf-8
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from functions.draw_trend import draw_trend
from functions.resources import get_ini_file
from ui_modules.dock_controller import DockController
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain
from ui_modules.charts import Trend


class StockExplorer(QMainWindow):
    """Main class for this application
    """

    def __init__(self):
        super().__init__()
        self.chart = None

        # ini file location
        self.file_ini = get_ini_file()
        print(self.file_ini)

        self.setWindowTitle('Stock Explorer')
        self.resize(1200, 800)
        self.setWindowIcon(
            QIcon(os.path.join('images', 'stock.png'))
        )

        self.dock_left = DockTicker()
        self.dock_bottom = DockController(self.dock_left)
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        # Toolbar
        toolbar = ToolBarMain()
        self.addToolBar(toolbar)

        # Dock for sticker codes
        self.dock_left.clicked.connect(self.on_ticker_selected)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.dock_left
        )

        # Dock for controller
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.dock_bottom
        )

        self.chart = Trend()
        self.setCentralWidget(self.chart)

        # set the first radio button selected
        rb = self.dock_left.get_first_button()
        if rb is not None:
            rb.setChecked(True)

    def on_ticker_selected(self, code):
        """Signal handler for ticker code button click

        Args:
            code (int): ticker code
        """
        print(code)
        draw_trend(self.chart, code)

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        print('アプリケーションを終了します。')
        event.accept()  # let the window close


def main():
    """Main event loop
    """
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
