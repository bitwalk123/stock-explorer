import os
import pandas as pd
import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates as mdates

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QStatusBar,
)

from snippets.set_env import set_env
from structs.res import AppRes
from trade.auto_trade_test_01 import AutoTradeTest01
from ui.toolbar_dts import DTSToolBar


class ChartSimlator(FigureCanvas):
    fig = Figure()

    def __init__(self):
        super().__init__(self.fig)
        self.fig.subplots_adjust(
            top=0.94,
            bottom=0.06,
            left=0.1,
            right=0.99,
            hspace=0,
        )
        self.ax = self.fig.add_subplot(111)


    def clearAxes(self):
        self.ax.cla()

    def refreshDraw(self):
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax.grid()
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()


class DayTrendSimulator(QMainWindow):
    app_ver = '0.0.1'

    def __init__(self):
        super().__init__()
        dict_info = set_env()
        res = AppRes()
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
        self.chart = chart = ChartSimlator()
        self.setCentralWidget(chart)

    def on_draw(self, df: pd.DataFrame, title:str):
        self.chart.clearAxes()
        t = df.index[0]
        set_ymd = (t.year, t.month, t.day)
        t_noon = pd.to_datetime('%4d-%02d-%02d 12:00:00' % set_ymd)
        df1 = df[df.index < t_noon]
        df2 =df[df.index > t_noon]
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
        trade = AutoTradeTest01(t)
        end = len(df.index) - 1
        for t in df.index[:end]:
            price = df.loc[t]['Price']
            trade.update(t, price)

        print(trade.getSummary())
        print(trade.getResult())


def main():
    app = QApplication()
    ex = DayTrendSimulator()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
