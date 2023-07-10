from PySide6.QtWidgets import QWidget, QSizePolicy
from matplotlib_inline.backend_inline import FigureCanvas


class WinPlot(QWidget):
    def __init__(self):
        super().__init__()
        #self.setSizePolicy(
        #    QSizePolicy.Policy.Expanding,
        #    QSizePolicy.Policy.Expanding
        #)
