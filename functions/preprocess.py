import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls_trade import (
    select_date_open_from_trade_with_id_code_start_end,
    select_open_from_trade_with_id_code_start_end,
    select_volume_from_trade_with_id_code_start_end,
)
from functions.app_enum import PreProcessExcluded


class PreProcess():
    # INITIAL CONSTANT
    FACTOR_PRICE: float = 1200.0
    FACTOR_TOLERANCE: float = 0.3
    FACTOR_SPLIT: float = 1.5
    FACTOR_VOLUME: int = 1000000

    FLAG_EXCLUDE = None

    DAY1 = 24 * 60 * 60
    HOLIDAYS = 16

    def __init__(self, id_code: int, start: int, end: int):
        self.id_code = id_code
        self.minimum_n = self.get_min_data(start, end)
        self.data_n = 0
        self.start = start
        self.end = end
        self.date = 0
        self.price_open = 0
        self.price_open_pre = -1
        #self.open_median = 0
        self.open_latest = 0
        self.volume_median = 0

    def init(self, target_price: float, ratio_split: float, target_volume: int):
        self.FACTOR_PRICE = target_price
        self.FACTOR_SPLIT = ratio_split
        self.FACTOR_VOLUME = target_volume

    def IsExclude(self) -> bool:
        # Check volume
        if self.check_volume():
            return True
        # Check split
        if self.check_split():
            return True
        else:
            return False

    def IsTarget(self):
        list_date = list()
        list_open = list()
        #sql = select_open_from_trade_with_id_code_start_end(
        #    self.id_code, self.start, self.end
        #)
        sql = select_date_open_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            list_date.append(query.value(0))
            list_open.append(query.value(1))

        if len(list_open) == 0:
            self.FLAG_EXCLUDE = PreProcessExcluded.EMPTY
            return True

        date_latest = max(list_date)
        idx_latest = list_date.index(date_latest)
        self.open_latest = list_open[idx_latest]
        #self.open_median = int(statistics.median(list_open))
        if self.open_latest < self.FACTOR_PRICE * (1 - self.FACTOR_TOLERANCE):
            return False
        elif self.open_latest > self.FACTOR_PRICE * (1 + self.FACTOR_TOLERANCE):
            return False
        else:
            return True

    def check_volume(self):
        list_volume = list()
        sql = select_volume_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            list_volume.append(query.value(0))

        list_volume_2 = [k for k in list_volume if len(str(k)) > 0]
        self.data_n = len(list_volume_2)
        # print(self.data_n, self.minimum_n)
        if self.data_n == 0:
            self.FLAG_EXCLUDE = PreProcessExcluded.EMPTY
            return True

        if self.data_n < self.minimum_n:
            self.FLAG_EXCLUDE = PreProcessExcluded.FEW
            return True

        self.volume_median = int(statistics.median(list_volume))
        if self.volume_median < self.FACTOR_VOLUME:
            self.FLAG_EXCLUDE = PreProcessExcluded.VOLUME
            return True
        else:
            return False

    def check_split(self):
        """Determine if price split exists
            based on the split factor in specified period.
        """
        sql = select_date_open_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            self.date = query.value(0)
            self.price_open = query.value(1)
            if self.is_split():
                self.FLAG_EXCLUDE = PreProcessExcluded.SPLIT
                return True

            self.price_open_pre = self.price_open

        return False

    def get_min_data(self, start: int, end: int) -> int:
        return int(((end - start) / self.DAY1 * 5 / 7 - self.HOLIDAYS) * 0.9)

    def is_split(self) -> bool:
        flag_date = self.price_open_pre > 0
        flag_upper = self.price_open_pre / self.FACTOR_SPLIT > self.price_open
        flag_lower = self.price_open_pre * self.FACTOR_SPLIT < self.price_open
        return flag_date and (flag_upper or flag_lower)
