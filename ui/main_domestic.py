import re
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from funcs.draw import draw_chart
from structs.trend_object import TrendObj
from ui.statusbar_domestic import StatusbarDomesticTicker
from ui.sub_good_bad import SubGoodBad
from widgets.charts import Trend
from ui.dock_domestics import DockDomesticTickers
from widgets.dialog import DialogAlert
from widgets.tab_panels import TabPanelMain
from ui.toolbar_domestic import ToolBarDomesticStocks


class MainDomesticStocks(TabPanelMain):
    tab_label = '国内株式'

    def __init__(self, parent):
        super().__init__(parent)
        self.toolbar = None
        self.dock_right = None
        self.statusbar = None
        self.sub_good_bad = None

        self.init_ui()

    def init_ui(self):
        self.toolbar = toolbar = ToolBarDomesticStocks(self)
        toolbar.kabutanGoodBadRequested.connect(self.on_good_bad_requested)
        toolbar.periodUpdate.connect(self.on_period_update)
        toolbar.plotTypeUpdated.connect(self.on_plot_type_changed)
        toolbar.tickerDown.connect(self.on_ticker_down)
        toolbar.tickerEntered.connect(self.on_ticker_entered)
        toolbar.tickerUp.connect(self.on_ticker_up)
        toolbar.rakutenOneDayRankingRequested.connect(self.on_oneday_ranking_requested)
        self.addToolBar(toolbar)
        # Right Dock
        self.dock_right = dock_right = DockDomesticTickers(self)
        dock_right.tickerSelected.connect(self.on_disp_update)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock_right
        )
        # StatusBar
        self.statusbar = StatusbarDomesticTicker(self)
        self.statusbar.setSizeGripEnabled(True)
        self.setStatusBar(self.statusbar)

        # CandleStick chart as default
        chart = Trend()
        self.setCentralWidget(chart)
        # display first code at the first time
        code = dock_right.getTickerFirst()
        self.on_disp_update(code)

    def on_oneday_ranking_requested(self, content):
        # いちにち信用ランキング
        pattern_date = r'<p class="pgh-01 align-R">(.+?)更新</p>'
        list_date = re.findall(pattern_date, content, re.DOTALL)
        print(list_date[0])

        pattern_header = r'<th class="cell-01 align-C" scope="col">(.+?)</th>\s*<th class="cell-01 align-C" scope="col">(.+?)</th>\s*<th class="cell-01 align-C" scope="col">(.+?)</th>'
        list_header = re.findall(pattern_header, content, re.DOTALL)
        print(list(list_header[0]))

        pattern_content = r'<th class="cell-02 align-C">(\d+?)</th>\s*<td class="align-C">(.+?)</td>\s*<td>(.+?)</td>'
        list_content = re.findall(pattern_content, content, re.DOTALL)
        print(list_content)

    def on_disp_update(self, code: str):
        self.toolbar.updateTicker(code)
        self.dock_right.setCheck(code)

        start = self.toolbar.getStartDate()
        chart: Union[QWidget, Trend] = self.centralWidget()
        gtype = self.toolbar.getPlotType()

        obj: TrendObj = draw_chart(chart, code, start, gtype)
        self.statusbar.updateTicker(obj)

    def on_good_bad_requested(self, dict_df: dict):
        self.sub_good_bad = sub_good_bad = SubGoodBad(dict_df)
        sub_good_bad.codeSelected.connect(self.on_disp_update)
        sub_good_bad.show()

    def on_period_update(self):
        code = self.dock_right.getCurrentTicker()
        self.on_disp_update(code)

    def on_plot_type_changed(self):
        code = self.dock_right.getCurrentTicker()
        self.on_disp_update(code)

    def on_ticker_down(self):
        code = self.dock_right.setTickerDown()
        self.on_disp_update(code)

    def on_ticker_entered(self, code: str):
        if self.dock_right.updateTicker(code):
            self.on_disp_update(code)
        else:
            self.restore_no_ticker(code)

    def on_ticker_up(self):
        code = self.dock_right.setTickerUp()
        self.on_disp_update(code)

    def restore_no_ticker(self, code: str):
        dlg = DialogAlert()
        dlg.setText('There is no ticker, \'%s\'!' % code)
        dlg.exec()
        code_current = self.dock_right.getCurrentTicker()
        self.toolbar.updateTicker(code_current)
