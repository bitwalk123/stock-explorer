import pandas as pd

from typing import Union


class DayTrade:
    def __init__(self):
        self.code: Union[str, None] = None
        self.start: Union[str, None] = None
        self.end: Union[str, None] = None
        self.interval: Union[str, None] = None
        self.df: Union[pd.DataFrame, None] = None

    def getInterval(self) -> str:
        if self.interval == '１分足':
            return '1m'
        elif self.interval == '５分足':
            return '5m'
        else:
            return ''

    def getTicker(self, jpx=True) -> str:
        if jpx:
            return '%s.T' % self.code
        else:
            return self.code
