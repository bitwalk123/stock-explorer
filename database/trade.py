from PySide6.QtCore import (
    QObject,
    QThreadPool,
    Signal,
)

from database.trade_worker import DBTblTradeCheckDuplicateWorker
from functions.resources import get_threadpool, get_connection


class DBTblTrade(QObject):
    """class for managing ticker table in the database
    """
    finished = Signal(float)
    logMessage = Signal(str)
    updateProgress = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.threadpool: QThreadPool = get_threadpool()
        self.con = None

    def check_duplicate(self):
        """Update ticker table in database
        """
        self.con = get_connection()
        if not self.con.open():
            print('database can not be opened!')
            return

        # _____________________________________________________________________
        # Threading
        worker = DBTblTradeCheckDuplicateWorker()
        worker.signals.finished.connect(self.thread_completed)
        worker.signals.logMessage.connect(self.show_log)
        worker.signals.updateProgress.connect(self.update_progress)
        self.threadpool.start(worker)

    def show_log(self, msg: str):
        """Show message
        """
        self.logMessage.emit(msg)

    def thread_completed(self, elapsed):
        """Process for thread completed
        """
        if self.threadpool.activeThreadCount() > 0:
            print(
                'current thread count:',
                self.threadpool.activeThreadCount()
            )
            self.threadpool.waitForDone(-1)

        self.con.close()

        print('[main] finished updating! (%.3f sec)' % elapsed)
        self.logMessage.emit('finished updating!')
        self.finished.emit(float)

    def update_progress(self, progress: int):
        """Emit for updating progress
        """
        self.updateProgress.emit(progress)
