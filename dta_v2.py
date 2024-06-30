import os
import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from funcs.dta_funcs import dta_get_data_from_db1m
from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from structs.res import AppRes
from ui.statusbar_dta import DTAStatusBar
from ui.toolbar_dta import DTAToolBarPlus
from widgets.charts import ChartForAnalysis


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        dict_info = set_env()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (widh DB), DTA')
        self.setMinimumSize(1000, 700)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBarPlus()
        toolbar.clickedPlot.connect(self.on_plot)
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
        self.statusbar = DTAStatusBar()
        self.setStatusBar(self.statusbar)

    def on_plot(self, qdate: QDate):
        dict_id_code = get_dict_id_code()
        code = self.toolbar.getCode()
        id_code = dict_id_code[code]

        start = get_day_timestamp(qdate)
        end = get_day_timestamp(qdate.addDays(1))

        df = dta_get_data_from_db1m(id_code, start, end)
        print(df)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
