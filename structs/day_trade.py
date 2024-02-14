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

    def getCName(self) -> str:
        return get_cname_with_code(self.code)

    def getInterval(self) -> str:
        if self.interval == '１分足':
            return '1m'
        elif self.interval == '５分足':
            return '5m'
        else:
            return ''

    def getPrevClose(self) -> Union[float, None]:
        return get_previous_close(self.code, self.start)

    def getTicker(self, jpx=True) -> str:
        if jpx:
            return '%s.T' % self.code
        else:
            return self.code

    def getTitle(self) -> str:
        title = '%s (%s)\n%sチャート on %s' % (
            self.getCName(),
            self.code,
            self.interval,
            self.start
        )
        return title
