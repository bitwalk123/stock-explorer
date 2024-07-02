import os
import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar,
)

from funcs.dta_funcs import dta_get_data_from_db1m
from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from structs.dta import DTAObj, DTAType
from structs.res import AppRes
from ui.dock_dta import DTADockSlider
from ui.statusbar_dta import DTAStatusBar
from ui.toolbar_dta import DTAToolBarPlus
from widgets.charts import ChartForAnalysis, yaxis_fraction


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        dict_info = set_env()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (with DB), DTA')
        self.setMinimumSize(1000, 700)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBarPlus()
        toolbar.clickedPlot.connect(self.on_plot)
        toolbar.clickedSimulate.connect(self.on_simulate)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartForAnalysis()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Dock
        dock = DTADockSlider()
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        self.statusbar = DTAStatusBar()
        self.setStatusBar(self.statusbar)

    def get_dtaobj(self) -> DTAObj | None:
        dict_id_code = get_dict_id_code()
        code = self.toolbar.getCode()
        id_code = dict_id_code[code]
        qdate = self.toolbar.getDate()
        start = get_day_timestamp(qdate)
        end = get_day_timestamp(qdate.addDays(1))
        df = dta_get_data_from_db1m(id_code, start, end)

        if len(df) == 0:
            return None
        else:
            dtatype = DTAType.CANDLE1M
            date_str = '%s-%s-%s' % (qdate.year(), qdate.month(), qdate.day())
            dtaobj = DTAObj(dtatype, code, date_str, df)
            return dtaobj

    @staticmethod
    def get_ylim(dtaobj: DTAObj) -> tuple[float, float]:
        y_min = dtaobj.getYMin()
        y_max = dtaobj.getYMax()
        y_pad = (y_max - y_min) * 0.025

        ylim_min = y_min - y_pad
        ylim_max = y_max + y_pad

        return ylim_min, ylim_max

    def on_plot(self):
        dtaobj = self.get_dtaobj()
        if dtaobj is None:
            print('No data!')
            return
        dtaobj.updateMSG.connect(self.updateStatus)
        data = dtaobj.getPlotData(0, robust=False)

        chart: QWidget | ChartForAnalysis = self.centralWidget()
        chart.clearAxes()

        for ax in [chart.ax1, chart.ax2, chart.ax3]:
            self.set_hvlines(ax)
            ax.grid()

        chart.ax3.set_xlabel('Tokyo Market Opening [sec]')

        chart.ax1.set_ylabel('Standardized Price')
        chart.ax1.set_ylim(-4, 4)
        chart.ax2.set_ylabel('$dy$')
        chart.ax3.set_ylabel('$dy^2$')

        # _____________________________________________________________________
        # Scaled
        chart.ax1.scatter(data['x'], data['y_scaled'], s=1, c='#444')
        stock_ticker = dtaobj.getTicker()
        date_str = dtaobj.getDateStr()
        legend_str = '%s : %s' % (stock_ticker, date_str)
        # _____________________________________________________________________
        # Smoothing Spline
        chart.ax1.fill_between(data['xs'], data['ys'], alpha=0.05)
        chart.ax1.plot(data['xs'], data['ys'], lw=1, label=legend_str)
        chart.ax1.set_ylim(self.get_ylim(dtaobj))
        chart.ax1.legend(loc='best')

        # _____________________________________________________________________
        # 1st Derivatives
        chart.ax2.plot(data['xs'], data['dy1s'], lw=1)
        yaxis_fraction(chart.ax2)

        # _____________________________________________________________________
        # 2nd Derivatives
        chart.ax3.plot(data['xs'], data['dy2s'], lw=1)
        yaxis_fraction(chart.ax3)

        chart.refreshDraw()

    def on_simulate(self):
        chart: QWidget | ChartForAnalysis = self.centralWidget()
        chart.clearAxes()

        print('DEBUG!')
        chart.refreshDraw()

    def set_hvlines(self, ax: Axes):
        ax.axhline(y=0, linestyle='solid', lw=0.75, c='black')
        ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')

    def updateStatus(self, msg: str):
        self.statusbar.setStatusMSG(msg)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
