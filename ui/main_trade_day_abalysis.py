import os
from typing import Union
import pandas as pd

from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QProgressDialog,
    QWidget,
)
from scipy import interpolate

from funcs.trade_day_analysis import (
    calc_diff,
    check_peak,
    draw_square,
    plot_peak,
)
from mthreads.get_day_trade import GetDayTradeWorker
from structs.day_trade import DayTrade
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade_day_analysis import ToolBarTradeDayAnalysis
from widgets.charts import Trend
from widgets.dialog import DialogAlert


class MainTradeDayAnalysis(QMainWindow):

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.threadpool = QThreadPool()

        self.progress: Union[QProgressDialog, None] = None
        self.toolbar = None
        self.dock_bottom = None

        self.setWindowTitle('Day Trade Analysis')
        self.resize(1200, 700)

        self.toolbar = toolbar = ToolBarTradeDayAnalysis(self)
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

    def on_draw_chart(self, info: DayTrade):
        # Check if dataframe is empty.
        if len(info.df) == 0:
            self.no_data_found(info)
            return

        chart: QWidget | Trend = self.centralWidget()
        chart.clearAxes()

        x = info.df.index
        y = info.df['Close']
        chart.ax.plot(
            x, y,
            color='#222',
            marker='o',
            markersize=2,
            linewidth=0
        )

        f = interpolate.interp1d(x.map(pd.Timestamp.timestamp), y, kind='slinear')

        # _____________________________________________________________________
        # Morning session
        x1 = pd.date_range(*info.getTimeMorningRange(x), freq='0.1min')
        y1 = f(x1.map(pd.Timestamp.timestamp))
        chart.ax.plot(
            x1, y1,
            color='#888',
            linewidth=1
        )

        diff1 = calc_diff(y1)
        diff11 = [0] + diff1
        diff12 = diff1 + [0]
        peak1 = check_peak(diff11, diff12, y1)

        df1 = pd.DataFrame({
            'x': x1,
            'y': y1,
            'peak': peak1,
        })

        df1_top = df1[df1['peak'] == 'top']
        pcolor = 'blue'
        plot_peak(chart, df1_top, pcolor)

        df1_bottom = df1[df1['peak'] == 'bottom']
        pcolor = 'red'
        plot_peak(chart, df1_bottom, pcolor)

        df1_tb = df1.query('peak in ["top", "bottom"]')
        draw_square(chart, df1_tb)

        # _____________________________________________________________________
        # Afternoon session
        x2 = pd.date_range(*info.getTimeAfternoonRange(x), freq='0.1min')
        y2 = f(x2.map(pd.Timestamp.timestamp))
        chart.ax.plot(
            x2, y2,
            color='#888',
            linewidth=1
        )

        diff2 = calc_diff(y2)
        diff21 = [0] + diff2
        diff22 = diff2 + [0]
        peak2 = check_peak(diff21, diff22, y2)

        df2 = pd.DataFrame({
            'x': x2,
            'y': y2,
            'peak': peak2,
        })

        df2_top = df2[df2['peak'] == 'top']
        pcolor = 'blue'
        plot_peak(chart, df2_top, pcolor)

        df2_bottom = df2[df2['peak'] == 'bottom']
        pcolor = 'red'
        plot_peak(chart, df2_bottom, pcolor)

        df2_tb = df2.query('peak in ["top", "bottom"]')
        draw_square(chart, df2_tb)
        # _____________________________________________________________________
        # Plot decolation
        chart.ax.set_title(info.getTitle())
        chart.ax.set_ylabel('Price')
        chart.ax.yaxis.set_tick_params(labelright=True)
        chart.ax.grid()
        chart.refreshDraw()

        # Hide progress dialog
        self.progress_hide()

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
