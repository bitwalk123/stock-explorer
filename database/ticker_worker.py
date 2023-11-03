import time

from PySide6.QtCore import (
    QRunnable,
)
from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import (
    create_table_ticker,
    drop_table_ticker,
    insert_into_ticker_values,
)
from database.worker_signals import WorkerSignals
from functions.get_elapsed import get_elapsed
from functions.resources import get_tse_data


class DBTblTickerWorker(QRunnable):
    """thread worker class for table ticker creation in database
    """
    def __init__(self, query: QSqlQuery):
        super().__init__()
        self.signals = WorkerSignals()
        self.time_start = 0
        self.query = query

    def run(self):
        self.time_start = time.time()
        df_all = get_tse_data()

        list_market = [
            'グロース（内国株式）',
            'グロース（外国株式）',
            'スタンダード（内国株式）',
            'スタンダード（外国株式）',
            'プライム（内国株式）',
            'プライム（外国株式）',
        ]
        df_stock = df_all[df_all['市場・商品区分'].isin(list_market)].reset_index(drop=True)
        record_total = len(df_stock.index)

        sql = drop_table_ticker()
        self.query.exec(sql)
        sql = create_table_ticker()
        self.query.exec(sql)

        for count, row in enumerate(df_stock.index):
            series = df_stock.loc[row]
            sql = insert_into_ticker_values(series)
            self.query.exec(sql)

            # update progress
            progress = int((count + 1) * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)
