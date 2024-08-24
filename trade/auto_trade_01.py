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
        if (self.status == TradeStatus.PRE) or (self.status == TradeStatus.BREAK):
            self.status = TradeStatus.HOLD
            self.t0 = t
            self.price0 = price
            return

        delta = self.calcDelta(t, price)

        if not self.isValidTime(t):
            if self.status != TradeStatus.HOLD:
                self.disp_current(t, price, 'transaction/force')
                self.transaction(t, price, force=True)
                self.disp_current(t, price, 'transaction/end')
            return

        if self.status == TradeStatus.HOLD:
            if delta > 0:
                self.disp_current(t, price, 'buy')
                self.buy(t, price)
                self.disp_current(t, price, 'bought')
            elif delta < 0:
                self.disp_current(t, price, 'sell')
                self.sell(t, price)
                self.disp_current(t, price, 'sold')
            else:
                self.disp_current(t, price, 'hold/stay')
            return

        if self.status == TradeStatus.BOUGHT:
            if self.price_limit < price:
                self.disp_current(t, price, 'transaction/match')
                self.transaction(t, price)
                self.disp_current(t, price, 'transaction/end')
            else:
                self.disp_current(t, price, 'bought/stay')
            return

        if self.status == TradeStatus.SOLD:
            if price < self.price_limit:
                self.disp_current(t, price, 'transaction/match')
                self.transaction(t, price)
                self.disp_current(t, price, 'transaction/end')
            else:
                self.disp_current(t, price, 'sold/stay')
            return
