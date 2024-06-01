import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.interpolate import make_smoothing_spline

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar, QFileDialog, QWidget,
)

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from ui.dta import DTAToolBar
from widgets.charts import ChartForAnalysis


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DayTrendAnalyzer')
        self.setMinimumSize(1000, 400)

        # _____________________________________________________________________
        # Toolbar
        toolbar = DTAToolBar()
        toolbar.clickedOpen.connect(self.on_open)
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

    def on_open(self):
        dialog = QFileDialog()
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.preprocess(filename)

    def preprocess(self, filename: str):
        df = pd.read_pickle(filename)

        date_str = str(df.index[0].date())
        t_start_1 = pd.to_datetime(date_str + ' 09:00:00')
        t_start_2 = pd.to_datetime(date_str + ' 10:00:00')
        t_mid = pd.to_datetime(date_str + ' 12:00:00')

        df1 = df.loc[df.index[df.index < t_mid]]
        df2 = df.loc[df.index[df.index > t_mid]]

        df11 = df1.copy()
        df11.index = [(t - t_start_1).total_seconds() for t in df1.index]

        df21 = df2.copy()
        df21.index = [(t - t_start_2).total_seconds() for t in df2.index]

        df0 = pd.concat([df11, df21])

        x = df0.index
        y = stats.zscore(df0['Price'])

        t_start_0 = 0
        t_end_0 = 18000
        t_interval_0 = 30

        spl = make_smoothing_spline(x, y)
        xs = np.linspace(t_start_0, t_end_0, int((t_end_0 - t_start_0) / t_interval_0))

        chart: QWidget | ChartForAnalysis = self.centralWidget()
        chart.clearAxes()

        chart.ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')

        chart.ax.set_xlabel('Tokyo Market Open [sec]')
        chart.ax.set_ylabel('Standardized Price')

        chart.ax.xaxis.set_ticks(np.arange(0, 18001, 1800))
        chart.ax.set_ylim(-4, 4)

        # chart.ax.scatter(x, y, s=1, c='gray')
        chart.ax.plot(xs, spl(xs), lw=1)
        chart.ax.grid()
        # chart.ax.legend(loc='best')

        chart.refreshDraw()


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
