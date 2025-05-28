import pyqtgraph as pg
from pyqtgraph import DateAxisItem


class TrendGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__(
            axisItems={'bottom': DateAxisItem(orientation='bottom')}
        )

        self.showGrid(x=True, y=True, alpha=0.5)
