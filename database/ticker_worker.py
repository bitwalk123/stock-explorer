import time

from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)
from PySide6.QtSql import QSqlQuery

from functions.get_elapsed import get_elapsed
from functions.resources import get_tse_data


class WorkerSignals(QObject):
    finished = Signal(float)
    logMessage = Signal(str)
    updateProgress = Signal(int)


class DBTblTickerWorker(QRunnable):
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
        """
        list_market = [
            'プライム（内国株式）',
            'プライム（外国株式）',
        ]
        """
        df_stock = df_all[df_all['市場・商品区分'].isin(list_market)].reset_index(drop=True)
        record_total = len(df_stock.index)

        self.query.exec('DROP TABLE IF EXISTS ticker')
        sql = """
            CREATE TABLE ticker(
                id_ticker INTEGER PRIMARY KEY AUTOINCREMENT,
                '日付' INTEGER,
                'コード' INTEGER,
                '銘柄名' STRING,
                '市場・商品区分' STRING,
                '33業種コード' INTEGER,
                '33業種区分' STRING,
                '17業種コード' INTEGER,
                '17業種区分' STRING,
                '規模コード' STRING,
                '規模区分' STRING
            )
        """
        self.query.exec(sql)

        for count, row in enumerate(df_stock.index):
            series = df_stock.loc[row]
            sql = 'INSERT INTO ticker VALUES(NULL, %d, %d, "%s", "%s", %d, "%s", %d, "%s", "%s", "%s")' % (
                series['日付'],
                series['コード'],
                series['銘柄名'],
                series['市場・商品区分'],
                series['33業種コード'],
                series['33業種区分'],
                series['17業種コード'],
                series['17業種区分'],
                series['規模コード'],
                series['規模区分']
            )
            self.query.exec(sql)

            # update progress
            progress = int((count + 1) * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit(elapsed)
