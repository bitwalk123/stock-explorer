import os
import re
import sys
import numpy as np
import pandas as pd
from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QWidget,
)

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from structs.dta import DTAObj, DTAType
from structs.res import AppRes
from ui.toolbar_dta import DTAToolBar
from widgets.charts import ChartForAnalysis


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_dtaobj = list()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DTA, DayTrendAnalyzer')
        self.setMinimumSize(1000, 600)

        # _____________________________________________________________________
        # Toolbar
        toolbar = DTAToolBar()
        toolbar.clickedOpen.connect(self.on_open)
        toolbar.clickedPlot.connect(self.on_plot)
        toolbar.clickedClear.connect(self.on_clear)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartForAnalysis()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    def on_clear(self):
        self.list_dtaobj = list()
        self.on_plot()

    def on_plot(self):
        chart: QWidget | ChartForAnalysis = self.centralWidget()
        chart.clearAxes()

        chart.ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')
        chart.ax.set_xlabel('Tokyo Market Open [sec]')
        chart.ax.set_ylabel('Scaled Price')
        chart.ax.xaxis.set_ticks(np.arange(0, 18001, 1800))
        chart.ax.set_ylim(-4, 4)

        for dtaobj in self.list_dtaobj:
            ticker = dtaobj.getTicker()
            date_str = dtaobj.getDateStr()
            legend_str = '%s : %s' % (ticker, date_str)
            x = dtaobj.getX()
            y = dtaobj.getY()
            chart.ax.scatter(x, y, s=1, c='black')
            xs, ys = dtaobj.getSmoothingSpline()
            chart.ax.plot(xs, ys, lw=1, label=legend_str)

        chart.ax.grid()
        if len(self.list_dtaobj) > 0:
            chart.ax.legend(loc='best')

        chart.refreshDraw()

    def on_open(self):
        #dialog = QFileDialog()
        #if dialog.exec():
        #    filename = dialog.selectedFiles()[0]
        filenames, _ = QFileDialog.getOpenFileNames(
            None,
            'Select Day Trend Files',
            '',
            'All Files (*);;Pickle Files (*.pkl)',
        )
        if filenames:
            for filename in filenames:
                self.preprocess(filename)
                self.on_plot()

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
        self.list_dtaobj.append(dtaobj)
        self.list_dtaobj.sort(key=lambda dtaobj: dtaobj.getDateStr())


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
