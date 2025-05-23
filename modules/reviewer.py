import logging
import re

from PySide6.QtCore import QDate, QDateTime, QTime, QObject

from funcs.tide import get_hms
from structs.res import YMD


class ExcelReviewer(QObject):
    def __init__(self, list_ticker: list, dict_sheet: dict, ymd: YMD):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f"{__name__} initialized.")

        self.pattern = re.compile(r"^tick_(.+)$")

        self.list_ticker = list_ticker
        self.dict_sheet = dict_sheet
        self.day_target = QDate(ymd.year, ymd.month, ymd.day)

    def plot(self):
        list_tick = list()
        for name_sheet in self.dict_sheet.keys():
            if name_sheet != "Cover":
                list_tick.append(name_sheet)

        for name_tick, ticker in zip(list_tick, self.list_ticker):
            self.logger.info(f"ワークシート「{name_tick}」")
            df = self.dict_sheet[name_tick]
            dt_start = QDateTime(self.day_target, QTime(9, 0, 0))
            dt_end = QDateTime(self.day_target, QTime(15, 30, 0))
            ticker.setTimeRange(dt_start, dt_end)

            list_hms = [get_hms(str(t)) for t in df["Time"]]
            list_dt = list()
            for hms in list_hms:
                time_target = QTime(hms.hour, hms.minute, hms.second)
                dt_target = QDateTime(self.day_target, time_target)
                list_dt.append(dt_target)

            m = self.pattern.match(name_tick)
            if m:
                code = m.group(1)
            else:
                code = "Unknown"
            ticker.setTitle(code)

            for dt, y in zip(list_dt, df["Price"]):
                ticker.appendPoint(dt, y)
