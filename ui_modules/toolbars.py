import datetime as dt
import pandas as pd
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)

from functions.resources import get_standard_icon
from ui_modules.dlg_config import DlgConfig
from ui_modules.dlg_info_ticker import DlgInfoTicker
from widgets.combos import ComboTradeRange
from widgets.entries import EntryTicker


class ToolBarMain(QToolBar):
    periodUpdate = Signal()
    tickerUp = Signal()
    tickerDown = Signal()
    plotTypeUpdated = Signal()

    le_ticker = None
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
        self.le_ticker = EntryTicker()
        self.addWidget(self.le_ticker)

        # 期間
        lab_range = QLabel('期間')
        lab_range.setContentsMargins(10, 0, 5, 0)
        self.addWidget(lab_range)

        self.combo_range = ComboTradeRange()
        self.combo_range.currentIndexChanged.connect(self.on_selected_range_changed)
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
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.addWidget(hpad)

        # Type of plot
        lab_plottype = QLabel('プロット')
        lab_plottype.setContentsMargins(0, 0, 10, 0)
        self.addWidget(lab_plottype)
        #
        rb_candle = QRadioButton('Candle')
        rb_candle.setChecked(True)
        rb_candle.clicked.connect(self.on_plot_tyoe_changed)
        self.addWidget(rb_candle)
        #
        rb_open = QRadioButton('Open')
        rb_open.clicked.connect(self.on_plot_tyoe_changed)
        self.addWidget(rb_open)
        #
        self.rb_group = QButtonGroup()
        self.rb_group.addButton(rb_open)
        self.rb_group.addButton(rb_candle)

        # Application config.
        but_conf = QToolButton()
        but_conf.setText('Configuration')
        but_conf.setToolTip('このアプリケーションの設定')
        icon_conf = get_standard_icon(self, 'SP_FileDialogDetailedView')
        but_conf.setIcon(icon_conf)
        but_conf.clicked.connect(self.show_conf_dialog)
        self.addWidget(but_conf)

    def get_start_date(self) -> int:
        sel = self.combo_range.currentText()
        today = int(pd.to_datetime(str(dt.date.today())).timestamp())
        year = 365 * 24 * 60 * 60
        if sel == '３ヵ月':
            return int(today - year / 4)
        elif sel == '６ヵ月':
            return int(today - year / 2)
        elif sel == '１年':
            return today - year
        elif sel == '２年':
            return today - 2 * year
        else:
            return -1

    def get_plot_type(self):
        rb = self.rb_group.checkedButton()
        return rb.text()

    def on_plot_tyoe_changed(self):
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            self.plotTypeUpdated.emit()

    def on_selected_range_changed(self, i):
        self.periodUpdate.emit()

    def on_ticker_info(self):
        code = self.parent.dock_left.get_current_ticker()
        dlg = DlgInfoTicker(code, parent=self)
        dlg.show()

    def on_ticker_down(self):
        self.tickerDown.emit()

    def on_ticker_up(self):
        self.tickerUp.emit()

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()

    def update_ticker(self, code):
        ticker = '%d.T' % code
        self.le_ticker.setText(ticker)
