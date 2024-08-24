import numpy as np
import pandas as pd

from structs.trade_status import TradeStatus
from trade.auto_trade import AutoTrade


class AutoTrade01(AutoTrade):
    """
    成行売買で、呼値で売却・買戻
    """
    def __init__(self, t: pd.Timestamp):
        super().__init__(t)

    def update(self, t: pd.Timestamp, price: np.float64):
        delta = self.calcDelta(t, price)

        if self.status == TradeStatus.PRE:
            self.status = TradeStatus.HOLD
            self.t0 = t
            self.price0 = price

        if not self.isValidTime(t):
            if self.status != TradeStatus.HOLD:
                self.transaction(t, price, force=True)
            return

        print(t, price, delta)
