import time

from PySide6.QtCore import QRunnable
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_id_code_from_ticker,
    get_sql_select_id_trade_date_open_from_trade_with_id_code,
    get_sql_delete_trade_with_id_trade,
)
from database.worker_signals import WorkerSignals
from functions.get_elapsed import get_elapsed


class DBTblTradeCheckDuplicateWorker(QRunnable):
    """thread worker class for table ticker creation in database
    """

    def __init__(self, query: QSqlQuery):
        super().__init__()
        self.signals = WorkerSignals()
        self.time_start = 0
        self.query = query

    def run(self):
        self.time_start = time.time()
        # record_total = len(df_stock.index)

        while self.query.next():
            id_code = self.query.value(0)
            print(id_code)

            list_date = list()
            sql2 = get_sql_select_id_trade_date_open_from_trade_with_id_code(id_code)
            query2 = QSqlQuery(sql2)
            while query2.next():
                id_trade = query2.value(0)
                date = query2.value(1)
                open = query2.value(2)
                if date in list_date:
                    print('duplicate', id_trade, date, open)
                    sql3 = get_sql_delete_trade_with_id_trade(id_trade)
                    query3 = QSqlQuery()
                    query3.exec(sql3)
                else:
                    list_date.append(date)

            # update progress
            # progress = int((count + 1) * 100 / record_total)
            # self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)
