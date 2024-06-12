from enum import Enum

import numpy as np
import pandas as pd
from scipy.interpolate import make_smoothing_spline

from funcs.dta_funcs import (
    dta_prep_candle1m,
    dta_prep_realtime,
)


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

        #self.array_x = np.empty(0)
        #self.array_y = np.empty(0)

        if dtatype == DTAType.REALTIME:
            self.array_x, self.array_y = dta_prep_realtime(self.date_str, self.df)
        elif dtatype == DTAType.CANDLE1M:
            self.array_x, self.array_y = dta_prep_candle1m(self.date_str, self.df)

        self.y_median = np.median(self.array_y)
        self.iqr = np.subtract(*np.percentile(self.array_y, [75, 25]))

    def getDataFrame(self) -> pd.DataFrame:
        return self.df

    def getDateStr(self) -> str:
        return self.date_str

    def getDTAType(self) -> DTAType:
        return self.dtatype

    def getTicker(self) -> str:
        return self.ticker

    def getSmoothingSpline(self) -> tuple[np.ndarray, np.ndarray]:
        t_start_0 = 0
        t_end_0 = 18000
        t_interval_0 = 1
        lam = 1

        spl = make_smoothing_spline(self.array_x, self.getYScaleed(), lam=lam)
        array_xs = np.linspace(t_start_0, t_end_0, int((t_end_0 - t_start_0) / t_interval_0))
        array_ys = spl(array_xs)

        return array_xs, array_ys

    def getX(self) -> np.ndarray:
        return self.array_x

    def getY(self) -> np.ndarray:
        return self.getYScaleed()

    def getYScaleed(self):
        return np.array([(y - self.y_median) / self.iqr for y in self.array_y])
