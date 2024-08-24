from enum import Enum


class TradeStatus(Enum):
    PRE = 0
    HOLD = 1
    BREAK = 2
    BOUGHT = 3
    SOLD = 4
    END = 5
