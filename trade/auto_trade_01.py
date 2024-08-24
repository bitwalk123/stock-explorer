from datetime import datetime

import numpy as np
import pandas as pd

from structs.trade_status import TradeStatus


class AutoTrade01:
    """
    タイムリーな成行売買で、かつ指定した額面で売却・買戻ができると仮定
    """
    def __init__(self):
        self.unit = 100
        self.result = 0
        self.status = TradeStatus.PRE
        self.t0: int | datetime = 0
        self.t1: int | datetime = 0
        self.t_noon: int | datetime = 0
        self.t2: int | datetime = 0
        self.price0 = 0

    def update(self, t: pd.Timestamp, price: np.float64):
        if self.status == TradeStatus.END:
            return

        if self.status != TradeStatus.PRE:
            if (self.t1 < t) and (t < self.t_noon):
                if (self.status == TradeStatus.BOUGHT) or (self.status == TradeStatus.SOLD):
                    self.earn(t, price)
                    return
                if self.status == TradeStatus.HOLD:
                    return
            if self.t2 < t:
                if (self.status == TradeStatus.BOUGHT) or (self.status == TradeStatus.SOLD):
                    self.earn(t, price)
                    self.status = TradeStatus.END
                    return
                if self.status == TradeStatus.HOLD:
                    return

        if self.status == TradeStatus.PRE:
            self.t1 = pd.to_datetime('%4d-%02d-%02d 11:29:00' % (t.year, t.month, t.day))
            self.t_noon = pd.to_datetime('%4d-%02d-%02d 12:00:00' % (t.year, t.month, t.day))
            self.t2 = pd.to_datetime('%4d-%02d-%02d 14:59:00' % (t.year, t.month, t.day))
            self.hold(t, price)
            return

        if self.status == TradeStatus.HOLD:
            if self.price0 < price:
                self.buy(t, price)
            elif self.price0 > price:
                self.sell(t, price)
            return

        if self.status == TradeStatus.BOUGHT:
            if self.price0 < price:
                self.earn(t, price)
            else:
                self.t0 = t
                self.price0 = price
            return

        if self.status == TradeStatus.SOLD:
            if self.price0 > price:
                self.earn(t, price)
            else:
                self.t0 = t
                self.price0 = price
            return

    def hold(self, t: pd.Timestamp, price: np.float64):
        self.status = TradeStatus.HOLD
        print('hold', t)
        self.t0 = t
        self.price0 = price

    def buy(self, t: pd.Timestamp, price: np.float64):
        self.status = TradeStatus.BOUGHT
        print('buy', t)
        self.t0 = t
        self.price0 = price

    def sell(self, t: pd.Timestamp, price: np.float64):
        self.status = TradeStatus.SOLD
        print('sell', t)
        self.t0 = t
        self.price0 = price

    def earn(self, t: pd.Timestamp, price: np.float64):
        gain = 0
        if self.status == TradeStatus.BOUGHT:
            gain = (price - self.price0) * self.unit
        elif self.status == TradeStatus.SOLD:
            gain = (self.price0 - price) * self.unit

        print('earn', t, gain)
        print()
        self.result += gain
        self.hold(t, price)

    def getResult(self):
        return self.result
