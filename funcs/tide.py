import datetime
import datetime as dt
import re

import pandas as pd

from PySide6.QtCore import QDate, QTimeZone, QDateTime, QTime

from structs.res import YMD, HMS


def get_dates(date_target: str) -> tuple[dt.datetime, dt.datetime]:
    """
    YYYY-MM-DD 文字列の指定した日付から、datetime.datetime 型の当日と翌日を生成
    :param date_target:
    :return:
    """
    dt_format = '%Y-%m-%d'
    dt_start = dt.datetime.strptime(date_target, dt_format)
    day1 = dt.timedelta(days=1)
    dt_end = dt_start + day1

    return dt_start, dt_end


def get_range_xaxis(df: pd.DataFrame) -> tuple:
    date_str = str(df.index[0].date())

    dt_left = pd.to_datetime(f"{date_str} 08:50:00")
    dt_right = pd.to_datetime(f"{date_str} 15:40:00")

    return dt_left, dt_right


def get_time_breaks(df: pd.DataFrame) -> tuple:
    """
    判定に使用する（日付付きの）時刻を取得

    :param df:
    :return:
    """
    date_str = str(df.index[0].date())
    # 前場終了時間
    dt_lunch_1 = pd.to_datetime(f"{date_str} 11:30:00")
    # 後場開始時間
    dt_lunch_2 = pd.to_datetime(f"{date_str} 12:30:00")
    # 後場ザラ場終了時間直前
    dt_pre_ca = pd.to_datetime(f"{date_str} 15:24:00")

    return dt_lunch_1, dt_lunch_2, dt_pre_ca


def get_yyyy_mm_dd(qdate: QDate) -> str:
    """
    QDate オブジェクトから YYYY-MM-DD の文字列を生成
    :param qdate:
    :return:
    str_year = "{:0=4}".format(qdate.year())
    str_month = "{:0=2}".format(qdate.month())
    str_day = "{:0=2}".format(qdate.day())
    date_target = f"{str_year}-{str_month}-{str_day}"

    return date_target
    """
    return f"{qdate.year():04}-{qdate.month():02}-{qdate.day():02}"



def get_yyyymmdd(qdate: QDate) -> str:
    """
    QDate オブジェクトから YYYYMMDD の文字列を生成
    :param qdate:
    :return:
    str_year = "{:0=4}".format(qdate.year())
    str_month = "{:0=2}".format(qdate.month())
    str_day = "{:0=2}".format(qdate.day())
    date_target = f"{str_year}{str_month}{str_day}"

    return date_target
    """
    return f"{qdate.year():04}{qdate.month():02}{qdate.day():02}"

def remove_tz_from_index(df: pd.DataFrame):
    """
    データフレームのタイムゾーン月時刻のインデックスからタイムゾーンを削除
    :param df:
    :return:
    """
    name_index = df.index.name
    df.index = [ts_jst.tz_localize(None) for ts_jst in df.index]
    df.index.name = name_index


def get_time_str(dt: pd.Timestamp) -> str:
    """
    Pandas の Timestamp 変数から時刻文字列 HH:MM:SS を取得
    :param dt:
    :return:
    """
    #return "{:0=2}:{:0=2}:{:0=2}".format(dt.hour, dt.minute, dt.second)
    return f"{dt.hour:02}:{dt.minute:02}:{dt.second:02}"


def get_msec_delta_from_utc():
    # 現在のローカルタイムゾーンを取得
    local_timezone = QTimeZone.systemTimeZone()

    # 現在の日時を取得
    current_datetime = QDateTime.currentDateTime()

    # ローカルタイムゾーンでのオフセット（秒単位）
    local_offset = local_timezone.offsetFromUtc(current_datetime)

    # msec 単位で返す
    return local_offset * 1000


def get_datetime_today() -> dict:
    dict_dt = dict()
    today = datetime.date.today()

    day_today = QDate(today.year, today.month, today.day)
    dict_dt["start"] = QDateTime(day_today, QTime(9, 0, 0))
    dict_dt["end_1h"] = QDateTime(day_today, QTime(11, 30, 0))
    dict_dt["start_2h"] = QDateTime(day_today, QTime(12, 30, 0))
    dict_dt["start_ca"] = QDateTime(day_today, QTime(15, 25, 0))
    dict_dt["end"] = QDateTime(day_today, QTime(15, 30, 0))
    return dict_dt


def get_ymd(excel_path: str) -> YMD:
    ymd = YMD()
    pattern = re.compile(r".+_([0-9]{4})([0-9]{2})([0-9]{2})\.xlsm")
    m = pattern.match(excel_path)
    if m:
        ymd.year = int(m.group(1))
        ymd.month = int(m.group(2))
        ymd.day = int(m.group(3))
    else:
        ymd.year = 1970
        ymd.month = 1
        ymd.day = 1
    return ymd


def get_hms(time_str: str) -> HMS:
    hms = HMS()
    pattern = re.compile(r"^([0-9]{1,2}):([0-9]{2}):([0-9]{2})$")
    m = pattern.match(time_str)
    if m:
        hms.hour = int(m.group(1))
        hms.minute = int(m.group(2))
        hms.second = int(m.group(3))
    else:
        hms.hour = 0
        hms.minute = 0
        hms.second = 0
    return hms
