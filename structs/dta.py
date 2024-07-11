from enum import Enum
from typing import Union

import numpy as np
import pandas as pd
from PySide6.QtCore import Signal, QObject
from scipy import integrate, interpolate
from scipy.interpolate import make_smoothing_spline

from funcs.dta_funcs import (
    dta_prep_candle1m,
    dta_prep_realtime,
)
from structs.param import ParamSmoothing


class DTAType(Enum):
    REALTIME = 1
    CANDLE1M = 2
    CANDLE5M = 3


class DTAObj(QObject):
    updateMSG = Signal(str)

    def __init__(
            self,
            dtatype: DTAType,
            ticker: str,
            date_str: str,
            df: pd.DataFrame
    ):
        super().__init__()
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

    def getPlotData(self, sigma: float, robust=True) -> dict:
        # _____________________________________________________________________
        # X data
        dist_data = dict()
        dist_data['x'] = self.x_array
        # _____________________________________________________________________
        # Scaled Y data
        if robust:
            if sigma == 0:
                sigma = self.iqr
            # Robust Scaling with median and IQR
            y_scaled = np.array([(y - self.y_median) / sigma for y in self.y_array])
        else:
            if sigma == 0:
                sigma = self.std
            # Standard Scaling with mean and standard deviation
            y_scaled = np.array([(y - self.y_mean) / sigma for y in self.y_array])

        self.y_max = np.max(y_scaled)
        self.y_min = np.min(y_scaled)
        dist_data['y_scaled'] = y_scaled
        # _____________________________________________________________________
        # Smoothing Spline
        param = ParamSmoothing()
        t_start = param.start
        t_end = param.end
        t_interval = param.interval

        if self.dtatype == DTAType.REALTIME:
            lam = param.lam2
        elif self.dtatype == DTAType.CANDLE1M:
            lam = param.lam
        else:
            lam = param.lam

        spl = make_smoothing_spline(self.x_array, y_scaled, lam=lam)
        dist_data['xs'] = xs = np.linspace(t_start, t_end, int((t_end - t_start) / t_interval))
        dist_data['ys'] = spl(xs)
        # _____________________________________________________________________
        # Integrals for Morning and Afternoon
        count = 0
        sum_morning = 0
        sum_afternoon = 0
        for h in dist_data['ys']:
            if count < t_end / 2:
                sum_morning += h
            else:
                sum_afternoon += h
            count += 1
        self.updateMSG.emit(
            'Area = (%d, %d)' % (round(sum_morning), round(sum_afternoon))
        )
        # _____________________________________________________________________
        # Derivatives
        dist_data['dy1s'] = interpolate.splev(xs, spl, der=1)
        dist_data['dy2s'] = interpolate.splev(xs, spl, der=2)

        return dist_data


class RTObj(QObject):
    def __init__(self, date_str: str, df: pd.DataFrame):
        super().__init__()
        self.date_str = date_str
        self.df = df
        self.time_left = pd.to_datetime(date_str + ' 08:50:00+09:00')
        self.time_mid = pd.to_datetime(date_str + ' 12:00:00+09:00')
        self.time_right = pd.to_datetime(date_str + ' 15:10:00+09:00')

    def area(self, df: pd.DataFrame, mean: float, sigma: float) -> float:
        x = np.array([t.timestamp() for t in df.index])
        y = np.array([(v - mean) / sigma for v in df['Price']])
        # return integrate.simpson(y, x=x)
        return integrate.trapezoid(y, x=x)

    def getDF1(self) -> pd.DataFrame:
        return self.df.loc[self.df.index[self.df.index < self.time_mid]]

    def getDF2(self) -> pd.DataFrame:
        return self.df.loc[self.df.index[self.df.index > self.time_mid]]

    def getXAxisRange(self) -> tuple[pd.Timestamp, pd.Timestamp]:
        return self.time_left, self.time_right

    def iqr(self) -> float:
        return np.subtract(*np.percentile(self.df['Price'], [75, 25]))

    def mean(self) -> float:
        return np.mean(self.df['Price'])

    def median(self) -> float:
        return np.median(self.df['Price'])

    def stdev(self) -> float:
        return np.std(self.df['Price'])
