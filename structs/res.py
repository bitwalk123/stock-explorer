import pandas as pd
from PySide6.QtWidgets import QStyle, QWidget


class AppRes:
    dir_excel = 'excel'
    dir_font = 'fonts'
    dir_image = 'images'
    dir_output = 'output'

    tse = 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls'

    def getBuiltinIcon(self, parent: QWidget, name: str):
        pixmap_icon = getattr(QStyle.StandardPixmap, 'SP_%s' % name)
        return parent.style().standardIcon(pixmap_icon)

    def getJPXTickerList(self) -> pd.DataFrame:
        return pd.read_excel(self.tse)


class YMD:
    year: int = 0
    month: int = 0
    day: int = 0

class HMS:
    hour: int = 0
    minute: int = 0
    second: int = 0
