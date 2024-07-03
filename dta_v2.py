import os
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

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
from widgets.charts import ChartForAnalysis
from widgets.dtaplot import DTAPlotBase, DTAPlotSim


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        dict_info = set_env()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (with DB), DTA')
        self.setMinimumSize(1000, 700)

        self.timer = QTimer()

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
        self.dock = DTADockSlider()
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock)

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
            date_str = '%04d-%02d-%02d' % (
                qdate.year(),
                qdate.month(),
                qdate.day()
            )
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
        chart: QWidget | ChartForAnalysis = self.centralWidget()
        self.plotobj = plotobj = DTAPlotSim(chart, dtaobj)
        plotobj.draw()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def update_data(self):
        if self.plotobj.shouldStopTimer():
            self.timer.stop()
        else:
            self.plotobj.update_data()

    def updateStatus(self, msg: str):
        self.statusbar.setStatusMSG(msg)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
