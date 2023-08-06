from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    """Signals for Worker class
    """
    finished = Signal(float)
    logMessage = Signal(str)
    updateProgress = Signal(int)
