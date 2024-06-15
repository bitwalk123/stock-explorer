from enum import Enum
from typing import Union

import numpy as np
import pandas as pd
from scipy import interpolate
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
        self.y_max = None
        self.y_min = None

        # self.array_x = np.empty(0)
        # self.array_y = np.empty(0)

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

    def getIQR(self) -> float:
        return self.iqr

    def getTicker(self) -> str:
        return self.ticker

    def getSmoothingSpline(self, iqr: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        t_start_0 = 0
        t_end_0 = 18000
        t_interval_0 = 1
        lam = 1

        spl = make_smoothing_spline(self.array_x, self.getYScaleed(iqr), lam=lam)
        array_xs = np.linspace(t_start_0, t_end_0, int((t_end_0 - t_start_0) / t_interval_0))
        array_ys = spl(array_xs)

        array_dy1s = interpolate.splev(array_xs, spl, der=1)
        array_dy2s = interpolate.splev(array_xs, spl, der=2)

        return array_xs, array_ys, array_dy1s, array_dy2s

    def getX(self) -> np.ndarray:
        return self.array_x

    def getY(self, iqr: float) -> np.ndarray:
        return self.getYScaleed(iqr)

    def getYMax(self) -> Union[float, None]:
        return self.y_max

    def getYMin(self) -> Union[float, None]:
        return self.y_min

    def getYScaleed(self, iqr: float):
        if iqr == 0:
            iqr = self.iqr

        y_array = np.array([(y - self.y_median) / iqr for y in self.array_y])
        self.y_max = np.max(y_array)
        self.y_min = np.min(y_array)

        return y_array
