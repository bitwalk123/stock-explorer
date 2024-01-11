import os

from PySide6.QtCore import Signal, Qt, QUrl
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QIcon,
    QKeySequence,
    QShortcut,
)
from PySide6.QtWidgets import (
    QMenu,
    QToolButton, QMainWindow,
)

from funcs.tide import get_past_date
from structs.res import AppRes
from ui.browser import NewsGoodBad
from widgets.labels import Label
from widgets.tab_panels import TabPanelMain
from widgets.toolbar_main import ToolBarMain
from widgets.combos import ComboTradeRange
from widgets.entries import EntryTicker
from widgets.pads import HPad


class ToolBarDomesticStocks(ToolBarMain):
    goodbadRequested = Signal(dict)
    periodUpdate = Signal()
    plotTypeUpdated = Signal()
    tickerDown = Signal()
    tickerEntered = Signal(str)
    tickerUp = Signal()

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.parent = parent
        self.res = res = AppRes()
        self.web = None
        self.action_grp: QActionGroup = None

        # Ticker
        lab_ticker = Label('銘柄')
        lab_ticker.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_ticker)

        self.ent_ticker = ent_ticker = EntryTicker()
        ent_ticker.returnPressed.connect(
            self.on_ticker_entered
        )
        self.addWidget(ent_ticker)

        lab_range = Label('期間')
        lab_range.setContentsMargins(10, 0, 5, 0)
        self.addWidget(lab_range)

        self.combo_range = combo_range = ComboTradeRange()
        combo_range.currentIndexChanged.connect(
            self.on_selected_range_changed
        )
        self.addWidget(combo_range)

        self.addSeparator()

        but_up = QToolButton()
        but_up.setContentsMargins(0, 0, 0, 0)
        but_up.setToolTip('前のコード')
        icon_up = QIcon(os.path.join(res.getImagePath(), 'arrow_up.png'))
        but_up.setIcon(icon_up)
        but_up.clicked.connect(self.on_ticker_up)
        self.addWidget(but_up)
        # Shortcut
        key_up = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        key_up.activated.connect(self.on_ticker_up)

        # Go down ticker
        but_down = QToolButton()
        but_down.setContentsMargins(0, 0, 0, 0)
        but_down.setToolTip('次のコード')
        icon_down = QIcon(os.path.join(res.getImagePath(), 'arrow_down.png'))
        but_down.setIcon(icon_down)
        but_down.clicked.connect(self.on_ticker_down)
        self.addWidget(but_down)
        # Shortcut
        key_down = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        key_down.activated.connect(self.on_ticker_down)

        # Separator
        hpad = HPad()
        self.addWidget(hpad)

        # Type of plot
        but_plottype = QToolButton()
        icon_plottype = QIcon(os.path.join(res.getImagePath(), 'chart.png'))
        but_plottype.setIcon(icon_plottype)
        but_plottype.setToolTip('プロット・タイプ')
        self.addWidget(but_plottype)

        menu_plottype = QMenu(self)
        but_plottype.setMenu(menu_plottype)
        but_plottype.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        self.gen_menuitem_plottype(menu_plottype)

        # Separator
        self.addSeparator()

        but_kabutan = QToolButton()
        icon_kabutan = QIcon(os.path.join(res.getImagePath(), 'kabutan.png'))
        but_kabutan.setIcon(icon_kabutan)
        but_kabutan.setToolTip('かぶたん')
        but_kabutan.clicked.connect(self.on_click_kabutan)
        self.addWidget(but_kabutan)

        # Separator
        self.addSeparator()

        but_rakuten = QToolButton()
        icon_rakuten = QIcon(os.path.join(res.getImagePath(), 'rakuten.png'))
        but_rakuten.setIcon(icon_rakuten)
        but_rakuten.setToolTip('楽天証券')
        but_rakuten.clicked.connect(self.on_click_rakuten)
        self.addWidget(but_rakuten)

        # Separator
        self.addSeparator()

        # Prediction viewer
        but_pred = QToolButton()
        but_pred.setToolTip('予測値の閲覧')
        icon_pred = QIcon(os.path.join(res.getImagePath(), 'predict.png'))
        but_pred.setIcon(icon_pred)
        # but_pred.clicked.connect(self.show_predictions)
        self.addWidget(but_pred)

        # Separator
        self.addSeparator()

        but_budget = QToolButton()
        icon_budget = QIcon(os.path.join(res.getImagePath(), 'budget.png'))
        but_budget.setIcon(icon_budget)
        but_budget.setToolTip('実現利益')
        but_budget.clicked.connect(self.on_click_budget)
        self.addWidget(but_budget)

        # Separator
        self.addSeparator()

        # Application config.
        but_conf = QToolButton()
        but_conf.setToolTip('このアプリケーションの設定')
        icon_conf = QIcon(os.path.join(res.getImagePath(), 'setting.png'))
        but_conf.setIcon(icon_conf)
        # but_conf.clicked.connect(self.show_conf_dialog)
        self.addWidget(but_conf)

    def gen_menuitem_plottype(self, menu: QMenu):
        # for Candle chart
        action_candle = QAction('Candle')
        action_candle.setCheckable(True)
        action_candle.setChecked(True)
        menu.addAction(action_candle)
        # for Open chart
        action_open = QAction('Open')
        action_open.setCheckable(True)
        action_open.setEnabled(True)
        menu.addAction(action_open)
        # for Close chart
        action_close = QAction('Close')
        action_close.setCheckable(True)
        action_close.setEnabled(True)
        menu.addAction(action_close)
        # for Open - Close chart
        action_close_open = QAction('Close - Open')
        action_close_open.setCheckable(True)
        action_close_open.setEnabled(True)
        menu.addAction(action_close_open)
        # _____________________________________________________________________
        # ActionButton group
        self.action_grp = action_grp = QActionGroup(self)
        action_grp.triggered.connect(self.on_plot_type_changed)
        action_grp.addAction(action_candle)
        action_grp.addAction(action_open)
        action_grp.addAction(action_close)
        action_grp.addAction(action_close_open)

    def getPlotType(self) -> str:
        action: QAction = self.action_grp.checkedAction()
        return action.text()

    def getStartDate(self):
        sel = self.combo_range.currentText()
        return get_past_date(sel)

    def on_click_kabutan(self):
        self.web = web = NewsGoodBad(
            self.res.getURLKabutanKoaku(),
            self.res.getJScriptInnerHTML()
        )
        web.goodbadRequested.connect(self.on_goodbadRequested)
        web.show()

    def on_click_budget(self):
        pass

    def on_click_rakuten(self):
        pass

    def on_goodbadRequested(self, dict_df: dict):
        self.goodbadRequested.emit(dict_df)

    def on_plot_type_changed(self):
        self.plotTypeUpdated.emit()

    def on_selected_range_changed(self):
        self.periodUpdate.emit()

    def on_ticker_down(self):
        self.tickerDown.emit()

    def on_ticker_entered(self):
        entered: str = self.ent_ticker.text()
        self.tickerEntered.emit(entered)

    def on_ticker_up(self):
        self.tickerUp.emit()

    def updateTicker(self, code: str):
        ticker = '%s' % code
        self.ent_ticker.setText(ticker)
