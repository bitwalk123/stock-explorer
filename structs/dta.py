from enum import Enum

import numpy as np
import pandas as pd

from funcs.dta_funcs import dta_prep_realtime, dta_smoothing_spline


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

        self.array_x = np.array(list())
        self.array_y = np.array(list())

        if dtatype == DTAType.REALTIME:
            self.array_x, self.array_y = dta_prep_realtime(self.date_str, self.df)

    def getDataFrame(self) -> pd.DataFrame:
        return self.df

    def getDateStr(self) -> str:
        return self.date_str

    def getDTAType(self) -> DTAType:
        return self.dtatype

    def getTicker(self) -> str:
        return self.ticker

    def getSmoothingSpline(self) -> tuple[np.ndarray, np.ndarray]:
        return dta_smoothing_spline(self.array_x, self.array_y)

    def getX(self) -> np.ndarray:
        return self.array_x

    def getY(self) -> np.ndarray:
        return self.array_y
