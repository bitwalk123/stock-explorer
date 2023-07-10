# Reference
# https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class WinPlot(FigureCanvasQTAgg):

    def __init__(self):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        # self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
