import re

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

    def getDate(self) -> Union[list, str]:
        date_pattern = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})')
        m = date_pattern.match(self.start)
        if m:
            yy = int(m.group(1))
            mm = int(m.group(2))
            dd = int(m.group(3))
            return [yy, mm, dd]
        else:
            return self.start

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

    def isJPX(self) -> bool:
        return self.jpx
