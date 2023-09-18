from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_date_open_from_trade_with_id_code_start_end


class preProcess():
    factor_split = 1.5

    def __init__(self, id_code: int, start:int, end:int):
        self.id_code = id_code
        self.start = start
        self.end = end
        self.date = 0
        self.price_open = 0
        self.price_open_pre = -1

    def is_split(self) -> bool:
        flag_date = self.price_open_pre > 0
        flag_upper = self.price_open_pre / self.factor_split > self.price_open
        flag_lower = self.price_open_pre * self.factor_split < self.price_open
        return flag_date and (flag_upper or flag_lower)

    def check(self) -> bool:
        sql = get_sql_select_date_open_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            self.date = query.value(0)
            self.price_open = query.value(1)
            if self.is_split():
                return True
            self.price_open_pre = self.price_open

        return False
