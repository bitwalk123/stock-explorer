import os
import re
import sys
import pandas as pd
from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QWidget,
)

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from structs.dta import DTAObj, DTAType
from structs.res import AppRes
from ui.statusbar_dta import DTAStatusBar
from ui.toolbar_dta import DTAToolBar
from widgets.charts import ChartForVerify02


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_dtaobj = list()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer, DTA')
        self.setMinimumSize(1000, 400)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBar()
        toolbar.checkChanged.connect(self.on_plot)
        toolbar.clickedBack.connect(self.on_back)
        toolbar.clickedClear.connect(self.on_clear)
        toolbar.clickedForward.connect(self.on_forward)
        toolbar.clickedOpen.connect(self.on_open)
        toolbar.clickedPlot.connect(self.on_plot)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartForVerify02()
        self.setCentralWidget(chart)
        self.on_plot()

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        self.statusbar = DTAStatusBar()
        self.setStatusBar(self.statusbar)

    def is_robust(self) -> bool:
        return self.toolbar.isRobust()

    def get_ax1_ylim(self) -> tuple[float, float]:
        obj_min = min(self.list_dtaobj, key=lambda obj: obj.getYMin())
        obj_max = max(self.list_dtaobj, key=lambda obj: obj.getYMax())

        y_min = obj_min.getYMin()
        y_max = obj_max.getYMax()
        y_pad = (y_max - y_min) * 0.025

        ax1_ylim_min = y_min - y_pad
        ax1_ylim_max = y_max + y_pad

        return ax1_ylim_min, ax1_ylim_max

    def get_iqr_max(self) -> float:
        dtaobj_max: DTAObj = max(self.list_dtaobj, key=lambda obj: obj.getIQR())
        iqr_max = dtaobj_max.getIQR()
        return iqr_max

    def get_std_max(self) -> float:
        dtaobj_max: DTAObj = max(self.list_dtaobj, key=lambda obj: obj.getSTD())
        std_max = dtaobj_max.getSTD()
        return std_max

    def on_back(self):
        pass

    def on_clear(self):
        self.list_dtaobj = list()
        self.on_plot()

    def on_forward(self):
        pass

    def on_open(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            None,
            'Select Day Trend Files',
            '',
            'Pickle Files (*.pkl);;All Files (*)',
        )
        if filenames:
            # Add object
            for filename in filenames:
                self.preprocess(filename)
            # Plot chart
            self.on_plot()

    def on_plot(self):
        chart: QWidget | ChartForVerify02 = self.centralWidget()
        chart.clearAxes()

        chart.ax.set_xlabel('Tokyo Market Opening [sec]')
        chart.ax.set_ylim(-4, 4)

        if len(self.list_dtaobj) > 0:
            if self.is_robust():
                sigma_max = self.get_iqr_max()
                chart.ax.set_ylabel('Robust Scaled Price')
            else:
                sigma_max = self.get_std_max()
                chart.ax.set_ylabel('Standardized Price')
        else:
            sigma_max = 0
            chart.ax.set_ylabel('Price')

        for dtaobj in self.list_dtaobj:
            data = dtaobj.getPlotData(sigma_max, robust=self.is_robust())
            # _________________________________________________________________
            # Scaled
            chart.ax.bar(
                data['xs'],
                data['ys']
            )
            for i, delta in enumerate(data['ys']):
                if delta > 0:
                    color = '#eef'
                elif delta < 0:
                    color = '#fee'
                else:
                    color = 'gray'
                chart.ax.get_children()[i].set_color(color)

            chart.ax.scatter(data['x'], data['y_scaled'], s=1, c='#444')
            stock_ticker = dtaobj.getTicker()
            date_str = dtaobj.getDateStr()
            legend_str = '%s : %s' % (stock_ticker, date_str)
            # _________________________________________________________________
            # Smoothing Spline
            chart.ax.plot(data['xs'], data['ys'], lw=0.75, label=legend_str)

        if len(self.list_dtaobj) > 0:
            chart.ax.legend(loc='best')
            chart.ax.set_ylim(self.get_ax1_ylim())
            chart.ax.axhline(y=0, linestyle='solid', lw=0.75, c='black')
            chart.ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')
            chart.ax.grid()

        chart.refreshDraw()

    def preprocess(self, filename: str):
        df = pd.read_pickle(filename)
        # _____________________________________________________________________
        # check if filename is for realtime
        p_rt = re.compile(r'.+/(.{4})_(\d{4}-\d{2}-\d{2})\.pkl$')
        m = p_rt.match(filename)
        if m:
            dtatype = DTAType.REALTIME
            ticker = m.group(1)
            date_str = m.group(2)
            self.proprocess_append(dtatype, ticker, date_str, df)
            return
        # _____________________________________________________________________
        # check if filename is for candle in 1 minute
        p_c1m = re.compile(r'.*/(.+)_(\d{4}-\d{2}-\d{2})_\d{4}-\d{2}-\d{2}_1m\.pkl')
        m = p_c1m.match(filename)
        if m:
            dtatype = DTAType.CANDLE1M
            ticker = m.group(1)
            date_str = m.group(2)
            self.proprocess_append(dtatype, ticker, date_str, df)
            return

    def proprocess_append(self, dtatype, ticker, date_str, df):
        dtaobj = DTAObj(dtatype, ticker, date_str, df)
        dtaobj.updateMSG.connect(self.updateStatus)
        self.list_dtaobj.append(dtaobj)
        self.list_dtaobj.sort(key=lambda dtaobj: dtaobj.getDateStr())

    def updateStatus(self, msg: str):
        self.statusbar.setStatusMSG(msg)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
