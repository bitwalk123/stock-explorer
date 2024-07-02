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


class DTAPlotBase:
    def __init__(self, chart: ChartForAnalysis, dtaobj: DTAObj):
        self.chart = chart
        self.dtaobj = dtaobj

    def draw(self):
        self.chart.clearAxes()

        data = self.dtaobj.getPlotData(0, robust=False)

        for ax in [self.chart.ax1, self.chart.ax2, self.chart.ax3]:
            self.set_hvlines(ax)
            ax.grid()

        self.chart.ax3.set_xlabel('Tokyo Market Opening [sec]')

        self.chart.ax1.set_ylabel('Standardized Price')
        self.chart.ax1.set_ylim(-4, 4)
        self.chart.ax2.set_ylabel('$dy$')
        self.chart.ax3.set_ylabel('$dy^2$')

        # _____________________________________________________________________
        # Scaled
        self.chart.ax1.scatter(data['x'], data['y_scaled'], s=1, c='#444')
        stock_ticker = self.dtaobj.getTicker()
        date_str = self.dtaobj.getDateStr()
        legend_str = '%s : %s' % (stock_ticker, date_str)
        # _____________________________________________________________________
        # Smoothing Spline
        self.chart.ax1.fill_between(data['xs'], data['ys'], alpha=0.05)
        self.chart.ax1.plot(data['xs'], data['ys'], lw=1, label=legend_str)
        self.chart.ax1.set_ylim(self.get_ylim(self.dtaobj))
        self.chart.ax1.legend(loc='best')

        # _____________________________________________________________________
        # 1st Derivatives
        self.chart.ax2.plot(data['xs'], data['dy1s'], lw=1)
        yaxis_fraction(self.chart.ax2)

        # _____________________________________________________________________
        # 2nd Derivatives
        self.chart.ax3.plot(data['xs'], data['dy2s'], lw=1)
        yaxis_fraction(self.chart.ax3)

        self.chart.refreshDraw()

    @staticmethod
    def get_ylim(dtaobj: DTAObj) -> tuple[float, float]:
        y_min = dtaobj.getYMin()
        y_max = dtaobj.getYMax()
        y_pad = (y_max - y_min) * 0.025

        ylim_min = y_min - y_pad
        ylim_max = y_max + y_pad

        return ylim_min, ylim_max

    @staticmethod
    def set_hvlines(ax: Axes):
        ax.axhline(y=0, linestyle='solid', lw=0.75, c='black')
        ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')


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

    def on_plot(self):
        dtaobj = self.get_dtaobj()
        if dtaobj is None:
            print('No data!')
            return
        dtaobj.updateMSG.connect(self.updateStatus)
        chart: QWidget | ChartForAnalysis = self.centralWidget()
        plotobj = DTAPlotBase(chart, dtaobj)
        plotobj.draw()

    def on_simulate(self):
        dtaobj = self.get_dtaobj()
        if dtaobj is None:
            print('No data!')
            return
        dtaobj.updateMSG.connect(self.updateStatus)
        print('DEBUG!')

    def updateStatus(self, msg: str):
        self.statusbar.setStatusMSG(msg)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
