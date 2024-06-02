import numpy as np
import pandas as pd
from scipy import stats as stats
from scipy.interpolate import make_smoothing_spline
from sklearn.preprocessing import robust_scale


def dta_get_ref_times(date_str) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    # for morning session
    t1 = pd.to_datetime(date_str + ' 09:00:00')
    # for afternoon session
    t2 = pd.to_datetime(date_str + ' 10:00:00')
    # middle of lunchtime
    t3 = pd.to_datetime(date_str + ' 12:00:00')

    return t1, t2, t3


def dta_get_ref_times_JST(date_str) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    # for morning session
    t1_origin = pd.to_datetime(date_str + ' 09:00:00+09:00')
    t1_end = pd.to_datetime(date_str + ' 11:30:00+09:00')
    # for afternoon session
    t2_origin = pd.to_datetime(date_str + ' 09:59:00+09:00')
    t2_start = pd.to_datetime(date_str + ' 12:30:00+09:00')

    return t1_origin, t1_end, t2_origin, t2_start


def dta_prep_candle1m(date_str: str, df: pd.DataFrame) -> tuple[np.array, np.array]:
    t1_origin, t1_end, t2_origin, t2_start = dta_get_ref_times_JST(date_str)

    df1 = df.loc[df.index[df.index <= t1_end]]
    df2 = df.loc[df.index[df.index >= t2_start]]

    df11 = df1.copy()
    df11.index = [(t - t1_origin).total_seconds() for t in df1.index]

    df21 = df2.copy()
    df21.index = [(t - t2_origin).total_seconds() for t in df2.index]

    df0 = pd.concat([df11, df21])

    array_x = np.array([x for x in df0.index])
    array_y = np.array([y for y in stats.zscore(df0['Close'])])

    return array_x, array_y


def dta_prep_realtime(date_str: str, df: pd.DataFrame) -> tuple[np.array, np.array]:
    t1, t2, t_mid = dta_get_ref_times(date_str)

    df1 = df.loc[df.index[df.index < t_mid]]
    df2 = df.loc[df.index[df.index > t_mid]]

    df11 = df1.copy()
    df11.index = [(t - t1).total_seconds() for t in df1.index]

    df21 = df2.copy()
    df21.index = [(t - t2).total_seconds() for t in df2.index]

    df0 = pd.concat([df11, df21])

    array_x = np.array([x for x in df0.index])
    #array_y = np.array([y for y in stats.zscore(df0['Price'])])
    array_y = np.array([y for y in robust_scale(df0['Price'])])

    return array_x, array_y


def dta_smoothing_spline(
        array_x: np.ndarray,
        array_y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    t_start_0 = 0
    t_end_0 = 18000
    t_interval_0 = 1
    lam = 1

    spl = make_smoothing_spline(array_x, array_y, lam=lam)
    array_xs = np.linspace(t_start_0, t_end_0, int((t_end_0 - t_start_0) / t_interval_0))
    array_ys = spl(array_xs)

    return array_xs, array_ys
