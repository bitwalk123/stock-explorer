# Reference
# https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        # self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
