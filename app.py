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
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from functions.alert import alert_no_ticker
from functions.draw_trend import draw_trend
from functions.get_ini_file import get_ini_file
from functions.numeric import is_num
from ui_modules.dock_controller import DockController
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain
from widgets.charts import Trend


class StockExplorer(QMainWindow):
    """Main class for this application
    """
    __version__ = '0.1.0'
    __build__ = '20231124'

    def __init__(self):
        super().__init__()
        self.chart = None

        # ini file location
        self.file_ini = get_ini_file()
        print(self.file_ini)

        self.setWindowTitle('Stock Explorer')
        self.resize(1200, 600)
        icon = QIcon(os.path.join('images', 'stock.png'))
        self.setWindowIcon(icon)

        # Initialize instances of UI components
        self.toolbar = ToolBarMain(self)
        self.dock_left = DockTicker()
        self.dock_bottom = DockController(self.toolbar, self.dock_left)

        self.init_ui()

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def init_ui(self):
        """Initialize UI
        """
        # Toolbar
        self.toolbar.periodUpdate.connect(self.on_period_update)
        self.toolbar.tickerDown.connect(self.on_ticker_down)
        self.toolbar.tickerEntered.connect(self.on_ticker_entered)
        self.toolbar.tickerUp.connect(self.on_ticker_up)
        self.toolbar.plotTypeUpdated.connect(self.on_chart_type_update)
        self.addToolBar(self.toolbar)

        # Dock for sticker codes
        self.dock_left.clicked.connect(self.on_disp_update)
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

        navtoolbar = NavigationToolbar(self.chart, self)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar
        )

        # Set the first radio button selected
        rb = self.dock_left.get_first_button()
        if rb is not None:
            rb.setChecked(True)

    def on_chart_type_update(self):
        code = self.dock_left.get_current_ticker()
        self.on_disp_update(code)

    def on_disp_update(self, code):
        """Signal handler for ticker code button click

        Args:
            code (int): ticker code
        """
        self.toolbar.update_ticker(code)
        self.dock_bottom.update_ticker(code)
        start = self.toolbar.get_start_date()
        gtype = self.toolbar.get_plot_type()
        draw_trend(self.chart, code, start, gtype)

    def on_period_update(self):
        """Signal handler for period range combobox changed
        """
        code = self.dock_left.get_current_ticker()
        self.on_disp_update(code)

    def on_ticker_down(self):
        """Move ticker down
        """
        self.dock_left.get_ticker_down()

    def on_ticker_entered(self, ticker: str):
        if is_num(ticker):
            code = int(ticker)
            if not self.dock_left.update_ticker(code):
                self.restore_no_ticker(ticker)
        else:
            self.restore_no_ticker(ticker)

    def on_ticker_up(self):
        """Move ticker up
        """
        self.dock_left.get_ticker_up()

    def restore_no_ticker(self, ticker):
        alert_no_ticker(ticker)
        code = self.dock_left.get_current_ticker()
        self.toolbar.update_ticker(code)

    def update_code(self, code: int):
        self.toolbar.update_ticker(code)
        if not self.dock_left.update_ticker(code):
            self.restore_no_ticker(str(code))


def main():
    """Main event loop
    """
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
