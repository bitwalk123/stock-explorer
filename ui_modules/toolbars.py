from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QRadioButton,
    QToolBar,
    QToolButton,
)

from functions.get_past_date import get_past_date
from functions.get_standard_icon import get_standard_icon
from ui_modules.dlg_predictions import DlgPredictions
from ui_modules.dlg_config import DlgConfig
from ui_modules.dlg_info_ticker import DlgInfoTicker
from widgets.combos import ComboTradeRange
from widgets.entries import EntryTicker
from widgets.widgets import HPad


class ToolBarMain(QToolBar):
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

        self.init_ui()

    def init_ui(self):
        # Ticker
        lab_ticker = QLabel('銘柄')
        lab_ticker.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_ticker)
        self.ent_ticker = EntryTicker()
        self.ent_ticker.returnPressed.connect(
            self.on_ticker_entered
        )
        self.addWidget(self.ent_ticker)

        # 期間
        lab_range = QLabel('期間')
        lab_range.setContentsMargins(10, 0, 5, 0)
        self.addWidget(lab_range)

        self.combo_range = ComboTradeRange()
        self.combo_range.currentIndexChanged.connect(
            self.on_selected_range_changed
        )
        self.addWidget(self.combo_range)

        self.addSeparator()

        # Go up ticker
        but_up = QToolButton()
        icon_up = get_standard_icon(self, 'SP_ArrowUp')
        but_up.setIcon(icon_up)
        but_up.clicked.connect(self.on_ticker_up)
        self.addWidget(but_up)
        # Shortcut
        key_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        key_up.activated.connect(self.on_ticker_up)

        # Go down ticker
        but_down = QToolButton()
        icon_down = get_standard_icon(self, 'SP_ArrowDown')
        but_down.setIcon(icon_down)
        but_down.clicked.connect(self.on_ticker_down)
        self.addWidget(but_down)
        # Shortcut
        key_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        key_down.activated.connect(self.on_ticker_down)

        # Ticker Information
        but_info = QToolButton()
        icon_info = get_standard_icon(self, 'SP_MessageBoxInformation')
        but_info.setIcon(icon_info)
        but_info.clicked.connect(self.on_ticker_info)
        self.addWidget(but_info)

        # 余白のスペーサ
        hpad = HPad()
        self.addWidget(hpad)

        # Type of plot
        lab_plottype = QLabel('プロット')
        lab_plottype.setContentsMargins(0, 0, 10, 0)
        self.addWidget(lab_plottype)
        #
        rb_candle = QRadioButton('Candle')
        rb_candle.setChecked(True)
        rb_candle.clicked.connect(self.on_plot_type_changed)
        self.addWidget(rb_candle)
        #
        rb_open = QRadioButton('Open')
        rb_open.clicked.connect(self.on_plot_type_changed)
        self.addWidget(rb_open)
        #
        self.rb_group = QButtonGroup()
        self.rb_group.addButton(rb_open)
        self.rb_group.addButton(rb_candle)

        self.addSeparator()
        # Prediction viewer
        but_pred = QToolButton()
        but_pred.setToolTip('予測値の閲覧')
        icon_pred = get_standard_icon(self, 'SP_FileDialogContentsView')
        but_pred.setIcon(icon_pred)
        but_pred.clicked.connect(self.show_predictions)
        self.addWidget(but_pred)

        # Application config.
        but_conf = QToolButton()
        # but_conf.setText('Configuration')
        but_conf.setToolTip('このアプリケーションの設定')
        icon_conf = get_standard_icon(self, 'SP_FileDialogDetailedView')
        but_conf.setIcon(icon_conf)
        but_conf.clicked.connect(self.show_conf_dialog)
        self.addWidget(but_conf)

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
