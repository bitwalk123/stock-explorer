import pandas as pd
from PySide6.QtWidgets import QStyle, QWidget


class AppRes:
    dir_excel = 'excel'
    dir_font = 'fonts'
    dir_image = 'images'
    tse = 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls'

    def getBuiltinIcon(self, parent: QWidget, name: str):
        pixmap_icon = getattr(QStyle.StandardPixmap, 'SP_%s' % name)
        return parent.style().standardIcon(pixmap_icon)

    def getJPXTickerList(self) -> pd.DataFrame:
        return pd.read_excel(self.tse)
