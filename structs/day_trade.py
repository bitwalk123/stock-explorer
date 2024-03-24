import pandas as pd

from typing import Union

from funcs.tbl_ticker import get_cname_with_code
from funcs.tbl_trade import get_previous_close


class DayTrade:
    def __init__(self):
        self.code: Union[str, None] = None
        self.start: Union[str, None] = None
        self.end: Union[str, None] = None
        self.interval: Union[str, None] = None
        self.df: Union[pd.DataFrame, None] = None
        self.jpx: Union[bool, None] = None

    def getCName(self) -> str:
        return get_cname_with_code(self.code)

    def getTimeMorningRange(self, x: pd.DatetimeIndex):
        t1 = str(min(x))
        t2 = self.start + ' 11:30:00+09:00'
        return t1, t2

    def getTimeAfternoonRange(self, x: pd.DatetimeIndex):
        t1 = self.start + ' 12:30:00+09:00'
        t2 = str(max(x))
        return t1, t2

    def getInterval(self) -> str:
        if self.interval == '１分足':
            return '1m'
        elif self.interval == '５分足':
            return '5m'
        else:
            return ''

    def getPrevClose(self) -> Union[float, None]:
        return get_previous_close(self.code, self.start)

    def getTicker(self) -> str:
        if self.jpx:
            return '%s.T' % self.code
        else:
            return self.code

    def getTitle(self) -> str:
        if self.jpx:
            title = '%s (%s)\n%sチャート on %s' % (
                self.getCName(),
                self.code,
                self.interval,
                self.start
            )
        else:
            title = '%s\n%sチャート on %s' % (
                self.code,
                self.interval,
                self.start
            )
        return title

    def isFullDataSet(self, df: pd.DataFrame) -> bool:
        if str(max(df.index)) == self.start + ' 14:59:00+09:00':
            return True
        else:
            return False

    def isJPX(self) -> bool:
        return self.jpx
