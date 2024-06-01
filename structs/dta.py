from enum import Enum

import pandas as pd


class DTAType(Enum):
    REALTIME = 1
    CANDLE1M = 2
    CANDLE5M = 3


class DTAObj:
    def __init__(
            self,
            dtatype: DTAType,
            ticker: str,
            date_str: str,
            df: pd.DataFrame
    ):
        self.dtatype = dtatype
        self.ticker = ticker
        self.date_str = date_str
        self.df = df

    def getDataFrame(self) -> pd.DataFrame:
        return self.df

    def getDateStr(self) -> str:
        return self.date_str

    def getDTAType(self) -> DTAType:
        return self.dtatype

    def getTicker(self) -> str:
        return self.ticker
