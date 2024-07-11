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

from funcs.dta_funcs import dta_get_data_from_dbrt
from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from structs.res import AppRes
from ui.statusbar_dta import DTAStatusBar
from ui.toolbar_dta import DTAToolBarRT
from widgets.charts import ChartRealtime


class DayTrendAnalyzerRT(QMainWindow):
    app_var = '3.0.0'

    def __init__(self):
        super().__init__()
        dict_info = set_env()
        mpl.rcParams['timezone']= 'Asia/Tokyo'

        self.date_str = None

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (RT with DB)')
        self.setMinimumSize(1000, 800)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBarRT()
        toolbar.clickedPlot.connect(self.on_plot)
        toolbar.clickedSimulate.connect(self.on_simulate)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartRealtime()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        self.statusbar = DTAStatusBar()
        self.setStatusBar(self.statusbar)

    def get_dataframe(self) -> pd.DataFrame:
        dict_id_code = get_dict_id_code()
        code = self.toolbar.getCode()
        id_code = dict_id_code[code]
        qdate = self.toolbar.getDate()
        self.date_str = '%4d-%02d-%02d' % (qdate.year(), qdate.month(), qdate.day())
        start = get_day_timestamp(qdate)
        end = get_day_timestamp(qdate.addDays(1))
        df = dta_get_data_from_dbrt(id_code, start, end)
        return df

    def on_plot(self):
        df = self.get_dataframe()
        if len(df) == 0:
            print('No data!')
            return

        print(df)
        chart: QWidget | ChartRealtime = self.centralWidget()
        time_left = pd.to_datetime(self.date_str + ' 08:50:00+09:00')
        time_mid = pd.to_datetime(self.date_str + ' 12:00:00+09:00')
        time_right = pd.to_datetime(self.date_str + ' 15:10:00+09:00')

        chart.clearAxes()
        df1 = df.loc[df.index[df.index < time_mid]]
        df2 = df.loc[df.index[df.index > time_mid]]

        if len(df1) > 0:
            chart.ax.plot(df1, c='C0', lw=1)
        if len(df2) > 0:
            chart.ax.plot(df2, c='C0', lw=1)

        chart.ax.set_xlim(time_left, time_right)
        chart.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        chart.ax.grid()
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
