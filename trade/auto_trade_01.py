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

    def update(self, t: pd.Timestamp, price: np.float64):
        if self.status == TradeStatus.PRE:
            self.status = TradeStatus.HOLD
            self.t0 = t
            self.price0 = price
            return

        delta = self.calcDelta(t, price)

        if not self.isValidTime(t):
            if self.status != TradeStatus.HOLD:
                self.transaction(t, price, force=True)
            return

        if self.status == TradeStatus.HOLD:
            if delta > 0:
                print(t, 'buy', self.price_own, self.price_limit, price, delta, self.result)
                self.buy(t, price)
                print(t, 'bought', self.price_own, self.price_limit, price, delta, self.result)
            elif delta < 0:
                print(t, 'sell', self.price_own, self.price_limit, price, delta, self.result)
                self.sell(t, price)
                print(t, 'sold', self.price_own, self.price_limit, price, delta, self.result)
            else:
                print(t, 'hold/stay', self.price_own, self.price_limit, price, delta, self.result)
            return

        if self.status == TradeStatus.BOUGHT:
            if self.price_limit < price:
                print(t, 'transaction/match', self.price_own, self.price_limit, price, delta, self.result)
                self.transaction(t, price)
                print(t, 'transaction/end', self.price_own, self.price_limit, price, delta, self.result)
            else:
                print(t, 'bought/stay', self.price_own, self.price_limit, price, delta, self.result)
            return

        if self.status == TradeStatus.SOLD:
            if price < self.price_limit:
                print(t, 'transaction/match', self.price_own, self.price_limit, price, delta, self.result)
                self.transaction(t, price)
                print(t, 'transaction/end', self.price_own, self.price_limit, price, delta, self.result)
            else:
                print(t, 'sold/stay', self.price_own, self.price_limit, price, delta, self.result)
            return