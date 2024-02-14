import os
from typing import Union

import mplfinance as mpf

from PySide6.QtCore import Qt, QThreadPool, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QProgressDialog

from mthreads.get_day_trade import GetDayTradeWorker
from structs.day_trade import DayTrade
from structs.res import AppRes
from ui.dock_navigator import DockNavigator
from ui.toolbar_trade_day import ToolBarTradeDay
from widgets.charts import Trend
from widgets.dialog import DialogAlert
from widgets.tab_panels import TabPanelMain


class MainTradeDay(TabPanelMain):
    tab_label = 'チャート（当日）'
    resizeRequested = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.res = AppRes()
        self.threadpool = QThreadPool()

        self.progress: Union[QProgressDialog, None] = None
        self.toolbar = None
        self.dock_bottom = None

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarTradeDay(self)
        toolbar.drawRequested.connect(self.on_get_day_trade)
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

    def on_draw_chart(self, info: DayTrade):
        # Check if dataframe is empty.
        if len(info.df) == 0:
            self.no_data_found(info)
            return

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
        close_prev = info.getPrevClose()
        if type(close_prev) is not None:
            chart.ax.axhline(
                y=close_prev,
                color='r',
                linewidth=1,
                linestyle=':',
                xmax=0.25
            )

        chart.ax.set_title(info.getTitle())
        chart.ax.set_ylabel('Price (JPY)')
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

    def on_resize_requested(self, flag: bool):
        self.resizeRequested.emit(flag)

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
        icon = QIcon(os.path.join(self.res.getImagePath(), 'hourglass.png'))
        progress.setWindowIcon(icon)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setCancelButton(None)
        progress.setWindowTitle('status')
        progress.setRange(0, 0)
        progress.show()
