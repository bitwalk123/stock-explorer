from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QRadioButton,
    QToolBar,
)

from functions.get_past_date import get_past_date
from ui_modules.dlg_predictions import DlgPredictions
from ui_modules.dlg_config import DlgConfig
from ui_modules.dlg_info_ticker import DlgInfoTicker


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

    def clear_ticker(self):
        self.ent_ticker.setText('')

    def get_start_date(self) -> int:
        sel = self.combo_range.currentText()
        return get_past_date(sel)

    def get_plot_type(self):
        rb = self.rb_group.checkedButton()
        return rb.text()

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

    def on_ticker_info(self):
        code = self.parent.dock_left.get_current_ticker()
        dlg = DlgInfoTicker(code, parent=self)
        dlg.show()

    def on_ticker_up(self):
        self.tickerUp.emit()

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()

    def show_predictions(self):
        dlg = DlgPredictions(parent=self)
        dlg.show()

    def update_ticker(self, code):
        ticker = '%d' % code
        self.ent_ticker.setText(ticker)
