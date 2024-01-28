import os
from typing import Union

import mplfinance as mpf
import pandas as pd

from PySide6.QtCore import Qt, Signal, QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QProgressBar, QProgressDialog

from funcs.tbl_ticker import get_cname_with_code
from funcs.tbl_trade import get_previous_close
from mthreads.get_day_trade import get_day_trade, GetDayTradeWorker
from structs.day_trade import DayTrade
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade_day import ToolBarTradeDay
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainTradeDay(TabPanelMain):
    tab_label = 'チャート（当日）'
    resizeRequested = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.threadpool = QThreadPool()

        self.progress: Union[QProgressDialog, None] = None
        self.toolbar = None
        self.dock_bottom = None
        self.res = AppRes()

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarTradeDay(self)
        toolbar.drawRequested.connect(self.on_draw)
        toolbar.resizeRequested.connect(self.on_resize_requested)
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

    def on_draw(self, info: DayTrade):
        worker = GetDayTradeWorker(info)
        worker.signals.finished.connect(self.on_draw_2)
        self.threadpool.start(worker)
        self.progress_show()

    def on_draw_2(self, info: DayTrade):
        self.progress_hide()
        chart: QWidget | Trend = self.centralWidget()
        chart.clearAxes()
        mpf.plot(
            info.df,
            type='candle',
            datetime_format='%H:%M',
            tight_layout=False,
            style=self.res.getCandleStyle(),
            ax=chart.ax
        )
        close_prev = get_previous_close(info.code, info.start)
        if type(close_prev) is not None:
            chart.ax.axhline(
                y=close_prev,
                color='r',
                linewidth=1,
                linestyle=':',
                xmax=0.25
            )

        cname = get_cname_with_code(info.code)
        title = '%s (%s)\n%sチャート on %s' % (
            cname, info.code, info.interval, info.start
        )
        chart.ax.set_title(title)
        chart.ax.set_ylabel('Price (JPY)')
        chart.ax.yaxis.set_tick_params(labelright=True)
        chart.ax.grid()
        chart.refreshDraw()

    def on_resize_requested(self, flag: bool):
        self.resizeRequested.emit(flag)

    def progress_hide(self):
        self.progress.hide()
        self.progress.deleteLater()

    def progress_show(self):
        self.progress = progress = QProgressDialog(
            labelText='Working...',
            parent=self
        )
        icon = QIcon(os.path.join(self.res.getImagePath(), 'hourglass.png'))
        progress.setWindowIcon(icon)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setCancelButton(None)
        progress.setWindowTitle('status')
        progress.setRange(0, 0)
        progress.show()
