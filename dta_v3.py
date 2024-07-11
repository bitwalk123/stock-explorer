import os
import pandas as pd
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow, QWidget,
)

import matplotlib as mpl
from matplotlib import dates as mdates
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from funcs.dta_funcs import dta_get_data_from_dbrt
from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from structs.dta import RTObj
from structs.res import AppRes
from ui.statusbar_dta import DTAStatusBar
from ui.toolbar_dta import DTAToolBarRT
from widgets.charts import ChartRealtimePlus


class DayTrendAnalyzerRT(QMainWindow):
    app_var = '3.0.0'

    def __init__(self):
        super().__init__()
        dict_info = set_env()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trend_realtime.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (RT with DB)')
        self.setMinimumSize(1000, 700)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBarRT()
        toolbar.clickedPlot.connect(self.on_plot)
        toolbar.clickedSimulate.connect(self.on_simulate)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartRealtimePlus()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        self.statusbar = DTAStatusBar()
        self.setStatusBar(self.statusbar)

    def get_dataframe(self) -> tuple[str, pd.DataFrame]:
        dict_id_code = get_dict_id_code()
        code = self.toolbar.getCode()
        id_code = dict_id_code[code]
        qdate = self.toolbar.getDate()
        start = get_day_timestamp(qdate)
        end = get_day_timestamp(qdate.addDays(1))
        df = dta_get_data_from_dbrt(id_code, start, end)
        date_str = '%4d-%02d-%02d' % (qdate.year(), qdate.month(), qdate.day())
        return date_str, df

    def on_plot(self):
        date_str, df = self.get_dataframe()
        if len(df) == 0:
            print('No data!')
            return
        rtobj = RTObj(date_str, df)

        # print(df)

        mean = rtobj.mean()
        sigma = rtobj.stdev()
        df1 = rtobj.getDF1()
        df2 = rtobj.getDF2()
        area1 = rtobj.area(df1, mean, sigma)
        area2 = rtobj.area(df2, mean, sigma)
        print('mean: %.1f, sigma: %.1f, morning: %.1f, afternoon: %.1f' % (mean, sigma, area1, area2))

        chart: QWidget | ChartRealtimePlus = self.centralWidget()
        chart.clearAxes()
        if len(df1) > 0:
            chart.ax.plot(df1, c='C0', lw=1)
            chart.ax.fill_between(df1.index, df1['Price'], mean, color='C0', alpha=0.1)
        if len(df2) > 0:
            chart.ax.plot(df2, c='C0', lw=1)
            chart.ax.fill_between(df2.index, df2['Price'], mean, color='C0', alpha=0.1)

        chart.ax.axhline(y=mean, c='r', lw=0.75, ls='-')

        chart.ax.set_xlim(rtobj.getXAxisRange())
        chart.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        chart.ax.xaxis.set_minor_locator(AutoMinorLocator())
        chart.ax.grid(axis='x', which='major', linestyle='-', color='gray')
        chart.ax.grid(axis='x', which='minor', linestyle='--', color='lightgray')

        chart.ax2 = chart.ax.twinx()
        chart.ax2.set_ylim(chart.ax.get_ylim())
        chart.ax2.set_yticks([])

        value_mean = [mean]
        chart.ax2.set_yticks(list(chart.ax2.get_yticks()) + value_mean)
        # Label for second y axis
        labels2 = [item.get_text() for item in chart.ax2.get_yticklabels()]
        n = len(labels2)
        labels2[n - 1] = '0'
        chart.ax2.set_yticklabels(labels2)
        # Color for second y axis
        y2ticklabels = chart.ax2.get_yticklabels()
        n = len(y2ticklabels)
        y2ticklabels[n - 1].set_color('red')

        chart.refreshDraw()

    def on_simulate(self):
        pass

    def updateStatus(self, msg: str):
        self.statusbar.setStatusMSG(msg)


def main():
    app = QApplication()
    ex = DayTrendAnalyzerRT()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
