import time

from PySide6.QtCore import QRunnable
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_id_code_from_ticker,
    get_sql_select_id_trade_date_open_from_trade_with_id_code,
    get_sql_delete_trade_with_id_trade, get_sql_select_count_from_ticker,
)
from database.worker_signals import WorkerSignals
from functions.get_elapsed import get_elapsed


class DBTblTradeCheckDuplicateWorker(QRunnable):
    """thread worker class for table ticker creation in database
    """

    def __init__(self, query1: QSqlQuery, query2: QSqlQuery, query3: QSqlQuery):
        super().__init__()
        self.signals = WorkerSignals()
        self.query1 = query1
        self.query2 = query2
        self.query3 = query3
        self.time_start = 0

    def run(self):
        self.time_start = time.time()
        sql1 = get_sql_select_count_from_ticker()
        self.query1.exec(sql1)
        record_total = 0
        while self.query1.next():
            record_total = self.query1.value(0)

        sql1 = get_sql_select_id_code_from_ticker()
        self.query1.exec(sql1)
        count = 0
        while self.query1.next():
            id_code = self.query1.value(0)
            count += 1

            list_date = list()
            sql2 = get_sql_select_id_trade_date_open_from_trade_with_id_code(id_code)
            self.query2.exec(sql2)
            while self.query2.next():
                id_trade = self.query2.value(0)
                date = self.query2.value(1)
                open = self.query2.value(2)
                if date in list_date:
                    print('duplicate', id_trade, date, open)
                    sql3 = get_sql_delete_trade_with_id_trade(id_trade)
                    self.query3.exec(sql3)
                else:
                    list_date.append(date)

            # update progress
            progress = int(count * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)
