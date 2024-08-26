import os
import pandas as pd
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QStatusBar,
)

from snippets.set_env import set_env
from structs.res import AppRes
from trade.auto_trade_test_02 import AutoTradeTest02
from ui.toolbar_dts import DTSToolBar
from widgets.charts import ChartSimulator
from widgets.models import PandasModel
from widgets.tables import PandasTableView


class DayTrendSimulator(QMainWindow):
    app_ver = '0.0.1'

    def __init__(self):
        super().__init__()
        dict_info = set_env()
        res = AppRes()

        self.win_result = None

        icon = QIcon(os.path.join(res.getImagePath(), 'simulator.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Simulator, DTS')

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTSToolBar()
        self.toolbar.folderClicked.connect(self.on_open)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # StatusBar
        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # _____________________________________________________________________
        # Chart
        self.chart = chart = ChartSimulator()
        self.setCentralWidget(chart)

    def on_draw(self, df: pd.DataFrame, title: str):
        self.chart.clearAxes()
        t = df.index[0]
        set_ymd = (t.year, t.month, t.day)
        t_noon = pd.to_datetime('%4d-%02d-%02d 12:00:00' % set_ymd)
        df1 = df[df.index < t_noon]
        df2 = df[df.index > t_noon]
        self.chart.ax.plot(df1, color='C0', alpha=0.5, linewidth=1)
        self.chart.ax.plot(df2, color='C0', alpha=0.5, linewidth=1)
        self.chart.ax.set_title(title)
        self.chart.refreshDraw()

    def on_open(self):
        dialog = QFileDialog()
        dialog.setNameFilters(['Pickle files (*.pkl)'])
        if dialog.exec():
            pklfile = dialog.selectedFiles()[0]
            df = pd.read_pickle(pklfile)
            title = os.path.splitext(os.path.basename(pklfile))[0]
            self.on_draw(df, title)
            self.simulation(df)

    def simulation(self, df: pd.DataFrame):
        t = df.index[0]
        trade = AutoTradeTest02(t)
        end = len(df.index) - 1
        for t in df.index[:end]:
            price = df.loc[t]['Price']
            trade.update(t, price)

        print('Total earning:', trade.getResult())

        df = trade.getSummary()
        self.show_result(df)

    def show_result(self, df: pd.DataFrame):
        self.win_result = win_result = QMainWindow()
        statusbar = QStatusBar()
        win_result.setStatusBar(statusbar)
        win_result.setWindowTitle('取引詳細')
        win_result.resize(800, 400)
        win_result.show()

        tbl = PandasTableView()
        win_result.setCentralWidget(tbl)
        model = PandasModel(df)
        tbl.setModel(model)


def main():
    app = QApplication()
    ex = DayTrendSimulator()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
