from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QRadioButton,
    QToolBar,
)


class ToolBarMainAbstract(QToolBar):
    periodUpdate = Signal()
    tickerDown = Signal()
    tickerEntered = Signal(str)
    tickerUp = Signal()
    plotTypeUpdated = Signal()

    ent_ticker = None
    combo_range = None
    rb_group = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def on_plot_type_changed(self):
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            self.plotTypeUpdated.emit()

    def on_selected_range_changed(self, i):
        self.periodUpdate.emit()

    def on_ticker_down(self):
        self.tickerDown.emit()

    def on_ticker_entered(self):
        entered: str = self.ent_ticker.text()
        self.tickerEntered.emit(entered)

    def on_ticker_up(self):
        self.tickerUp.emit()

    def update_ticker(self, code):
        ticker = '%d' % code
        self.ent_ticker.setText(ticker)
