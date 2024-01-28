import pandas as pd
import yfinance as yf
from PySide6.QtCore import Signal, QObject, QRunnable

from structs.day_trade import DayTrade


def get_day_trade(info: DayTrade) -> pd.DataFrame:
    df = yf.download(
        info.getTicker(),
        info.start,
        info.end,
        interval=info.getInterval()
    )
    # id_code = get_id_code_from_code(code)
    return df


class GetDayTradeWorkerSignals(QObject):
    progress = Signal(str)
    finished = Signal(DayTrade)


class GetDayTradeWorker(QRunnable):
    def __init__(self, info: DayTrade):
        super().__init__()
        self.signals = GetDayTradeWorkerSignals()
        self.info = info

    def run(self):
        df = get_day_trade(self.info)
        self.info.df = df
        self.signals.finished.emit(self.info)