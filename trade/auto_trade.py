import numpy as np
import pandas as pd
from PySide6.QtCore import QObject, Signal

from structs.trade_status import TradeStatus


class AutoTrade(QObject):
    madeContract = Signal()

    def __init__(self, t: pd.Timestamp):
        super().__init__()
        self.unit = 100  # 単元株数
        self.tick = 10  # 呼値
        self.price_own = 0  # 所持価格
        self.price_limit = 0  # 指値価格
        self.result = 0.0
        self.status = TradeStatus.PRE

        # Valid dealing time
        set_ymd = (t.year, t.month, t.day)
        self.t1 = pd.to_datetime('%4d-%02d-%02d 11:29:00' % set_ymd)
        self.t_noon = pd.to_datetime('%4d-%02d-%02d 12:00:00' % set_ymd)
        self.t2 = pd.to_datetime('%4d-%02d-%02d 14:59:00' % set_ymd)

        # Previous values
        self.t0 = 0
        self.price0 = 0

    def update(self, t: pd.Timestamp, price: np.float64):
        ...

    def hold(self, t: pd.Timestamp, price: np.float64):
        ...

    def buy(self, t: pd.Timestamp, price: np.float64):
        if self.price_own != 0:
            print('ERROR!')
            return

        self.price_own = price
        self.price_limit = price + self.tick
        self.status = TradeStatus.BOUGHT

    def sell(self, t: pd.Timestamp, price: np.float64):
        if self.price_own != 0:
            print('ERROR!')
            return

        self.price_own = price
        self.price_limit = price - self.tick
        self.status = TradeStatus.SOLD

    def transaction(self, t: pd.Timestamp, price: np.float64, force=False):
        if self.status == TradeStatus.BOUGHT:
            if force:
                delta = price - self.price_own
            else:
                delta = self.price_limit - self.price_own
            self.result += delta * self.unit
            self.price_own = 0
            self.price_limit = 0
            self.status = TradeStatus.HOLD
            return

        if self.status == TradeStatus.SOLD:
            if force:
                delta = self.price_own - price
            else:
                delta = self.price_own - self.price_limit
            self.result += delta * self.unit
            self.price_own = 0
            self.price_limit = 0
            self.status = TradeStatus.HOLD
            return

    def calcDelta(self, t: pd.Timestamp, price: np.float64):
        delta = price - self.price0
        self.t0 = t
        self.price0 = price
        return delta

    def getResult(self) -> float:
        return self.result

    def isValidTime(self, t: pd.Timestamp):
        if self.t1 < t < self.t_noon:
            return False
        elif self.t2 < t:
            return False
        else:
            return True
