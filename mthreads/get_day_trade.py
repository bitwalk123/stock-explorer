import pandas as pd
import yfinance as yf
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from structs.day_trade import DayTrade


def get_day_trade(info: DayTrade) -> pd.DataFrame:
    df = yf.download(
        info.getTicker(),
        start=info.start,
        end=info.end,
        interval=info.getInterval()
    )
    return df


class GetDayTradeWorkerSignal(QObject):
    finished = Signal(DayTrade)


class GetDayTradeWorker(QRunnable, GetDayTradeWorkerSignal):
    def __init__(self, info: DayTrade):
        super().__init__()
        self.info = info

    def run(self):
        df = get_day_trade(self.info)
        self.info.df = df
        self.finished.emit(self.info)
