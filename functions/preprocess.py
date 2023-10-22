import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_date_open_from_trade_with_id_code_start_end,
    get_sql_select_volume_from_trade_with_id_code_start_end,
)
from functions.app_enum import PreProcessEnum


class PreProcess():
    # INITIAL CONSTANT
    FACTOR_PRICE: float = 1000.0
    FACTOR_SPLIT: float = 1.5
    FACTOR_VOLUME: int = 10000

    def __init__(self, id_code: int, start: int, end: int):
        self.id_code = id_code
        self.start = start
        self.end = end
        self.date = 0
        self.price_open = 0
        self.price_open_pre = -1
        self.flag_exclude = None
        self.volume_median = 0

    def init(self, target_price: float, ratio_split: float, target_volume: int):
        self.FACTOR_PRICE = target_price
        self.FACTOR_SPLIT = ratio_split
        self.FACTOR_VOLUME = target_volume

    def is_split(self) -> bool:
        flag_date = self.price_open_pre > 0
        flag_upper = self.price_open_pre / self.FACTOR_SPLIT > self.price_open
        flag_lower = self.price_open_pre * self.FACTOR_SPLIT < self.price_open
        return flag_date and (flag_upper or flag_lower)

    def exclude(self) -> bool:
        # Check volume
        if self.check_volume():
            return True
        # Check split
        if self.check_split():
            return True
        else:
            return False

    def check_volume(self):
        list_volume = list()
        sql = get_sql_select_volume_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            list_volume.append(query.value(0))

        if len(list_volume) == 0:
            self.flag_exclude = PreProcessEnum.EMPTY
            return True

        self.volume_median = int(statistics.median(list_volume))
        if self.volume_median < self.FACTOR_VOLUME:
            self.flag_exclude = PreProcessEnum.VOLUME
            return True
        else:
            return False

    def check_split(self):
        """Determine if price split exists
            based on the split factor in specified period.
        """
        sql = get_sql_select_date_open_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            self.date = query.value(0)
            self.price_open = query.value(1)
            if self.is_split():
                self.flag_exclude = PreProcessEnum.SPLIT
                return True

            self.price_open_pre = self.price_open

        return False
