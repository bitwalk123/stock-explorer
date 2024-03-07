import os
import sys
import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

from PySide6.QtCore import (
    QThreadPool,
    Qt,
    Signal,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressDialog,
    QWidget,
)

from mthreads.get_day_trade import GetDayTradeWorker
from snippets.set_env import set_env
from structs.day_trade import DayTrade
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade_day_pred import ToolBarTradeDayPred
from widgets.charts import Trend
from widgets.dialog import DialogAlert


class DayTradePred(QMainWindow):
    resizeRequested = Signal(bool)

    def __init__(self):
        super().__init__()
        dict_info = set_env()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        icon = QIcon(os.path.join(res.getImagePath(), 'predict.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trade Prediction')

        self.toolbar = toolbar = ToolBarTradeDayPred(self)
        toolbar.drawRequested.connect(self.on_get_day_trade)
        self.addToolBar(toolbar)

        # CandleStick chart as default
        chart = Trend(gtype='Trend')
        self.setCentralWidget(chart)

        # Bottom Dock
        self.dock_bottom = dock_bottom = DockNavigator(self, chart)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )

        self.resize(1200, 700)

    def on_draw_chart(self, info: DayTrade):
        # Check if dataframe is empty.
        if len(info.df) == 0:
            self.no_data_found(info)
            return

        df = pd.DataFrame(
            {'Close': info.df['Close']},
            index=pd.to_datetime(info.df.index)
        )
        sma = df['Close'].rolling(window=10).mean()

        chart: QWidget | Trend = self.centralWidget()
        chart.clearAxes()
        chart.ax.plot(
            df.index,
            df['Close'],
            color='dodgerblue',
            marker='o',
            markeredgecolor='dodgerblue',
            markerfacecolor='cyan',
            markersize=2,
            linewidth=0.5
        )
        chart.ax.plot(
            df.index,
            sma,
            color='darkorange',
            linewidth=1
        )
        chart.ax.set_title(info.getTitle())
        chart.ax.set_ylabel('Price')
        chart.ax.yaxis.set_tick_params(labelright=True)
        chart.ax.grid()

        chart.refreshDraw()

        # Hide progress dialog
        self.progress_hide()

    @staticmethod
    def add_previous_close(chart, info):
        close_prev = info.getPrevClose()
        if type(close_prev) is not None:
            chart.ax.axhline(
                y=close_prev,
                color='r',
                linewidth=1,
                linestyle=':',
                xmax=0.25
            )

    def on_get_day_trade(self, info: DayTrade):
        worker = GetDayTradeWorker(info)
        worker.finished.connect(self.on_draw_chart)
        self.threadpool.start(worker)

        # Show progress dialog
        self.progress_show()

    def no_data_found(self, info: DayTrade):
        # Hide progress dialog
        self.progress_hide()

        # Warning dialog
        dlg = DialogAlert()
        dlg.setText('%s のデータがありませんでした。' % info.start)
        dlg.exec()

    def progress_hide(self):
        self.progress.hide()
        self.progress.deleteLater()

    def progress_show(self):
        self.progress = progress = QProgressDialog(
            labelText='Working...',
            parent=self
        )
        icon = QIcon(
            os.path.join(self.res.getImagePath(), 'hourglass.png')
        )
        progress.setWindowIcon(icon)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setCancelButton(None)
        progress.setWindowTitle('status')
        progress.setRange(0, 0)
        progress.show()


def main():
    app = QApplication(sys.argv)
    win = DayTradePred()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
