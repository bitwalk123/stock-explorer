import datetime as dt
import time
import yfinance as yf

from PySide6.QtCore import QRunnable
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    delete_trade_with_id_trade,
    insert_into_trade_values,
    select_count_from_ticker,
    select_id_code_from_ticker,
    select_id_trade_date_open_from_trade_with_id_code,
    select_id_code_code_from_ticker,
    select_max_date_from_trade_with_id_code,
)
from database.worker_signals import WorkerSignals
from functions.conv_timestamp2date import conv_timestamp2date_next
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
        sql1 = select_count_from_ticker()
        self.query1.exec(sql1)
        record_total = 0
        while self.query1.next():
            record_total = self.query1.value(0)

        count = 0
        sql1 = select_id_code_from_ticker()
        self.query1.exec(sql1)
        while self.query1.next():
            count += 1
            id_code = self.query1.value(0)

            list_date = list()
            sql2 = select_id_trade_date_open_from_trade_with_id_code(id_code)
            self.query2.exec(sql2)
            while self.query2.next():
                id_trade = self.query2.value(0)
                date = self.query2.value(1)
                open = self.query2.value(2)
                if date in list_date:
                    print('duplicate', id_trade, date, open)
                    sql3 = delete_trade_with_id_trade(id_trade)
                    self.query3.exec(sql3)
                else:
                    list_date.append(date)

            # update progress
            progress = int(count * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)

class DBTblTradeUpdateTradeWorker(QRunnable):
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
        end = dt.date.today()

        sql1 = select_count_from_ticker()
        self.query1.exec(sql1)
        record_total = 0
        while self.query1.next():
            record_total = self.query1.value(0)

        count = 0
        sql1 = select_id_code_code_from_ticker()
        self.query1.exec(sql1)
        while self.query1.next():
            count += 1

            id_code = self.query1.value(0)
            code = '%d.T' % self.query1.value(1)

            sql2 = select_max_date_from_trade_with_id_code(id_code)
            self.query2.exec(sql2)
            while self.query2.next():
                date_max = self.query2.value(0)
                if type(date_max) is not int:
                    continue
                start = conv_timestamp2date_next(date_max)
                print('\n', code)

                df = yf.download(code, start, end)
                if len(df) == 0:
                    continue
                for row in df.index:
                    timestamp = row.timestamp()
                    series = df.loc[row].copy()
                    series['Date'] = timestamp
                    sql3 = insert_into_trade_values(id_code, series)
                    self.query3.exec(sql3)

            # update progress
            progress = int(count * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)
