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

        if dtatype == DTAType.REALTIME:
            self.x_array, self.y_array = dta_prep_realtime(self.date_str, self.df)
        elif dtatype == DTAType.CANDLE1M:
            self.x_array, self.y_array = dta_prep_candle1m(self.date_str, self.df)

        self.y_median = np.median(self.y_array)
        self.y_mean = np.mean(self.y_array)
        self.iqr = np.subtract(*np.percentile(self.y_array, [75, 25]))
        self.std = np.std(self.y_array)

    def getDataFrame(self) -> pd.DataFrame:
        return self.df

    def getDateStr(self) -> str:
        return self.date_str

    def getDTAType(self) -> DTAType:
        return self.dtatype

    def getSTD(self) -> float:
        return self.std

    def getIQR(self) -> float:
        return self.iqr

    def getTicker(self) -> str:
        return self.ticker

    def getYMax(self) -> Union[float, None]:
        return self.y_max

    def getYMin(self) -> Union[float, None]:
        return self.y_min

    def getPlotData(self, iqr: float) -> dict:
        if iqr == 0:
            iqr = self.iqr

        # X data
        dist_data = dict()
        dist_data['x'] = self.x_array

        # Scaled Y data
        y_scaled = np.array([(y - self.y_median) / iqr for y in self.y_array])
        self.y_max = np.max(y_scaled)
        self.y_min = np.min(y_scaled)
        dist_data['y_scaled'] = y_scaled

        # Smoothing Spline
        t_start_0 = 0
        t_end_0 = 18000
        t_interval_0 = 1
        lam = 10 ** 5

        # lam : float, (:math:`\lambda \geq 0`)
        #             Regularization parameter.
        spl = make_smoothing_spline(self.x_array, y_scaled, lam=lam)
        # spl = make_smoothing_spline(self.array_x, y_scaled)
        dist_data['xs'] = xs = np.linspace(t_start_0, t_end_0, int((t_end_0 - t_start_0) / t_interval_0))
        dist_data['ys'] = spl(xs)

        count = 0
        sum1 = 0
        sum2 = 0
        for h in dist_data['ys']:
            if count < t_end_0 / 2:
                sum1 += h
            else:
                sum2 += h
            count += 1
        print('sum', round(sum1), round(sum2))

        dist_data['dy1s'] = interpolate.splev(xs, spl, der=1)
        dist_data['dy2s'] = interpolate.splev(xs, spl, der=2)

        return dist_data
