from enum import Enum


class TradeStatus(Enum):
    PRE = 0
    HOLD = 1
    BOUGHT = 2
    SOLD = 3
    END = 4
