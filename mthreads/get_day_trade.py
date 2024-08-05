import os

import pandas as pd
import yfinance as yf
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from structs.day_trade import DayTrade


def get_day_trade(info: DayTrade) -> pd.DataFrame:
    file_cache = 'cache/%s_%s_%s_%s.pkl' % (
        info.getTicker(), info.start, info.end, info.getInterval()
    )
    if os.path.isfile(file_cache):
        print('read from %s' % file_cache)
        df = pd.read_pickle(file_cache)
    else:
        print('read from Yahoo finance')
        df = yf.download(
            info.getTicker(),
            start=info.start,
            end=info.end,
            interval=info.getInterval()
        )
        if len(df) > 0:
            if info.isFullDataSet(df):
                df.to_pickle(file_cache)
            else:
                print(df)

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
