import pandas as pd

from funcs.tide import conv_date_string


class TrendObj():
    cname: str = None
    code: str = None
    df: pd.DataFrame = None
    date_from: str = None
    date_to: str = None
    num: int = None
    name_13sector: str = None
    volume: int = None

    def setCname(self, cname: str):
        self.cname = cname

    def setCode(self, code: str):
        self.code = code

    def setDataFrame(self, df: pd.DataFrame):
        self.df = df

    def setDateFrom(self, start: pd.Timestamp):
        self.date_from = conv_date_string(start)

    def setDateTo(self, end: pd.Timestamp):
        self.date_to = conv_date_string(end)

    def setNum(self, num: int):
        self.num = num

    def set13Sector(self, name_13sector: str):
        self.name_13sector = name_13sector

    def setVolume(self, volume: int):
        self.volume = volume

    def getCname(self) -> str:
        return self.cname

    def getCode(self) -> str:
        return self.code

    def getDataFrame(self) -> pd.DataFrame:
        return self.df

    def getDateFrom(self) -> str:
        return self.date_from

    def getDateTo(self) -> str:
        return self.date_to

    def getNum(self) -> int:
        return self.num

    def get13Sector(self) -> str:
        return self.name_13sector

    def getVolume(self) -> int:
        return self.volume
