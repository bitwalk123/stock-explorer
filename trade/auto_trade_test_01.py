import numpy as np
import pandas as pd

from structs.trade_status import TradeStatus
from trade.auto_trade_base import AutoTradeBase


class AutoTradeTest01(AutoTradeBase):
    """
    成行売買で、呼値 (tick) で売却・買戻
    損切り (Loss-cut) 条件無し
    """

    def __init__(self, t: pd.Timestamp):
        super().__init__(t)

    def update(self, t: pd.Timestamp, price: np.float64):
        if self.isFirstDeal(t, price):
            return

        delta = self.getDelta(t, price)

        if not self.isValidTime(t):
            if (self.status == TradeStatus.BOUGHT) or (self.status == TradeStatus.SOLD):
                self.dispCurrent(t, price, 'TRANSACTION/force')
                self.transaction(t, price, force=True)
                self.dispCurrent(t, price, 'TRANSACTION/end')
            return

        if self.status == TradeStatus.HOLD:
            if delta > 0:
                self.dispCurrent(t, price, 'BUY')
                self.buy(t, price)
                self.dispCurrent(t, price, 'BOUGHT')
            elif delta < 0:
                self.dispCurrent(t, price, 'SELL')
                self.sell(t, price)
                self.dispCurrent(t, price, 'SOLD')
            else:
                self.dispCurrent(t, price, 'HOLD/stay')
            return

        if self.status == TradeStatus.BOUGHT:
            if self.price_limit < price:
                self.dispCurrent(t, price, 'TRANSACTION/match')
                self.transaction(t, price)
                self.dispCurrent(t, price, 'TRANSACTION/end')
            else:
                self.dispCurrent(t, price, 'BOUGHT/stay')
            return

        if self.status == TradeStatus.SOLD:
            if price < self.price_limit:
                self.dispCurrent(t, price, 'TRANSACTION/match')
                self.transaction(t, price)
                self.dispCurrent(t, price, 'TRANSACTION/end')
            else:
                self.dispCurrent(t, price, 'SOLD/stay')
            return
