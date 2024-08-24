import numpy as np
import pandas as pd

from structs.trade_status import TradeStatus
from trade.auto_trade import AutoTrade


class AutoTrade01(AutoTrade):
    """
    成行売買で、呼値 (tick) で売却・買戻
    損切り (Loss-cut) 条件無し
    """

    def __init__(self, t: pd.Timestamp):
        super().__init__(t)

    def disp_current(self, t: pd.Timestamp, price: np.float64, delta: float, title: str):
        print(t, title, self.price_own, self.price_limit, price, delta, self.result)

    def update(self, t: pd.Timestamp, price: np.float64):
        if self.status == TradeStatus.PRE:
            self.status = TradeStatus.HOLD
            self.t0 = t
            self.price0 = price
            return

        delta = self.calcDelta(t, price)

        if not self.isValidTime(t):
            if self.status != TradeStatus.HOLD:
                self.disp_current(t, price, delta, 'transaction/force')
                self.transaction(t, price, force=True)
                self.disp_current(t, price, delta, 'transaction/end')
            return

        if self.status == TradeStatus.HOLD:
            if delta > 0:
                #print(t, 'buy', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'buy')
                self.buy(t, price)
                #print(t, 'bought', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'bought')
            elif delta < 0:
                #print(t, 'sell', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'sell')
                self.sell(t, price)
                #print(t, 'sold', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'sold')
            else:
                #print(t, 'hold/stay', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'hold/stay')
            return

        if self.status == TradeStatus.BOUGHT:
            if self.price_limit < price:
                #print(t, 'transaction/match', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'transaction/match')
                self.transaction(t, price)
                #print(t, 'transaction/end', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'transaction/end')
            else:
                #print(t, 'bought/stay', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'bought/stay')
            return

        if self.status == TradeStatus.SOLD:
            if price < self.price_limit:
                #print(t, 'transaction/match', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'transaction/match')
                self.transaction(t, price)
                #print(t, 'transaction/end', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'transaction/end')
            else:
                #print(t, 'sold/stay', self.price_own, self.price_limit, price, delta, self.result)
                self.disp_current(t, price, delta, 'sold/stay')
            return
