import sys
from typing import Union

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

from funcs.draw import draw_chart
from funcs.tide import get_past_date
from snippets.set_env import set_env
from structs.trend_object import TrendObj
from widgets.charts import Trend


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        dict_info = set_env()

        chart = Trend()
        self.setCentralWidget(chart)

        self.on_disp_update('8035')

    def on_disp_update(self, code: str):
        chart: Union[QWidget, Trend] = self.centralWidget()

        start = get_past_date('３ヵ月')
        gtype = 'Candle'

        obj: TrendObj = draw_chart(chart, code, start, gtype)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
