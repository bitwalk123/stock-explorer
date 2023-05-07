import time

from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
    Slot,
)
from PySide6.QtSql import QSqlQuery

from functions.get_elapsed import get_elapsed
from functions.resources import get_tse_data


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread.
    """
    finished = Signal()
    logMessage = Signal(str)
    updateProgress = Signal(int)


class DBTblTickerWorker(QRunnable):
    def __init__(self, query: QSqlQuery):
        super().__init__()
        self.signals = WorkerSignals()
        self.query = query

    @Slot()
    def run(self):
        self.time_start = time.time()
        df_all = get_tse_data()

        """
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
        df_stock = df_all[df_all['市場・商品区分'].isin(list_market)].reset_index(drop=True)
        record_total = len(df_stock.index)

        for count, row in enumerate(df_stock.index):
            series = df_stock.loc[row]
            sql = 'INSERT INTO ticker values(NULL, %d, %d, "%s", "%s", %d, "%s", %d, "%s", "%s", "%s")' % (
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
            progress = int(count * 100 / record_total)
            self.signals.updateProgress.emit(progress)

        elapsed = get_elapsed(self.time_start)
        print('[thread] finished updating! (%.3f sec)' % elapsed)
        self.signals.finished.emit()
