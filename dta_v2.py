import datetime
import os
import pandas as pd
import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QMainWindow, QApplication

from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from sqls.sql_trade_day import sql_sel_all_from_trade1m_with_dates_id_code_datetimes
from structs.db_info import DBInfo
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

        df = self.get_data_from_db(id_code, start, end)
        print(df)

    def get_data_from_db(self, id_code: int, start: int, end: int) -> pd.DataFrame:
        list_series = list()
        con = DBInfo.get_connection()
        if con.open():
            query = QSqlQuery()
            sql = sql_sel_all_from_trade1m_with_dates_id_code_datetimes(id_code, start, end)
            query.exec(sql)
            while query.next():
                date_time = query.value(0)  # "Datetime"
                dict_stock = dict()
                dict_stock['Open'] = query.value(1)  # "Open"
                dict_stock['High'] = query.value(2)  # "High"
                dict_stock['Low'] = query.value(3)  # "Low"
                dict_stock['Close'] = query.value(4)  # "Close"
                dict_stock['Volume'] = query.value(5)  # "Volume"
                series = pd.Series(data=dict_stock, name=date_time)
                list_series.append(series)
            con.close()

        if len(list_series) > 0:
            df = pd.concat(list_series, axis=1).T
            list_dt = [datetime.datetime.fromtimestamp(ts, datetime.timezone.utc) for ts in df.index]
            list_dt_jst = [dt.astimezone(datetime.timezone(datetime.timedelta(hours=9))) for dt in list_dt]
            df.index = list_dt_jst
        else:
            df = pd.DataFrame({'Open': [], 'Low': [], 'High': [], 'Close': [], 'Volume': []})

        df.index.name = 'Datetime'

        return df


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
