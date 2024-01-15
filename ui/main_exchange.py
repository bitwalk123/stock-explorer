from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from funcs.draw import draw_chart
from structs.trend_object import TrendObj
from ui.dock_exchange import DockExchange
from ui.dock_navigator import DockNavigator
from ui.statusbar_exchange import StatusbarExchange
from ui.toolbar_exchange import ToolBarExchange
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainExchange(TabPanelMain):
    tab_label = '外国為替'

    def __init__(self, parent):
        super().__init__(parent)

        self.toolbar = None
        self.dock_right = None
        self.dock_bottom = None
        self.statusbar = None

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarExchange(self)
        toolbar.periodUpdate.connect(self.on_period_update)
        self.addToolBar(toolbar)
        # Right Dock
        self.dock_right = dock_right = DockExchange(self)
        # dock_right.currencySelected.connect(self.on_disp_update)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock_right
        )
        # StatusBar
        self.statusbar = StatusbarExchange(self)
        self.statusbar.setSizeGripEnabled(True)
        self.setStatusBar(self.statusbar)

        # CandleStick chart as default
        chart = Trend()
        self.setCentralWidget(chart)

        # Bottom Dock
        self.dock_bottom = dock_bottom = DockNavigator(self, chart)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )


        # display first code at the first time
        code = dock_right.getCurrentDefault()
        self.on_disp_update(code)

    def on_disp_update(self, currency: str):
        self.toolbar.updateCurrency(currency)
        self.dock_right.setCheck(currency)
        start = self.toolbar.getStartDate()

        chart: Union[QWidget, Trend] = self.centralWidget()
        gtype = self.toolbar.getPlotType()

        obj: TrendObj = draw_chart(chart, currency, start, gtype)
        self.statusbar.updateCurrency(obj)

    def on_period_update(self):
        currency = self.dock_right.getCurrentCurrency()
        self.on_disp_update(currency)
