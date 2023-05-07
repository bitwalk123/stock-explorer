from PySide6.QtCore import (
    QObject,
    QThreadPool,
    Signal,
)
from PySide6.QtSql import QSqlQuery

from database.ticker_worker import DBTblTickerWorker
from functions.resources import (
    get_connection,
    get_info,
    get_threadpool,
)


class DBTblTicker(QObject):
    finished = Signal()
    logMessage = Signal(str)
    updateProgress = Signal(int)

    def __init__(self):
        super().__init__()
        self.threadpool: QThreadPool = get_threadpool()
        self.con = None

    def update(self):
        self.con = get_connection()
        dbname = get_info('db')
        self.con.setDatabaseName(dbname)
        if not self.con.open():
            print('database can not be opened!')
            return
        query = QSqlQuery()
        # _____________________________________________________________________
        # Threading
        worker = DBTblTickerWorker(query)
        worker.signals.finished.connect(self.thread_completed)
        worker.signals.logMessage.connect(self.show_log)
        worker.signals.updateProgress.connect(self.update_progress)
        self.threadpool.start(worker)

    def show_log(self, msg: str):
        self.logMessage.emit(msg)

    def thread_completed(self):
        print('[main] finished updating!')
        self.con.close()

        if self.threadpool.activeThreadCount() > 0:
            print('current thread count:', self.threadpool.activeThreadCount())
            self.threadpool.waitForDone(-1)

        self.logMessage.emit('finished updating!')
        self.finished.emit()

    def update_progress(self, progress: int):
        self.updateProgress.emit(progress)
