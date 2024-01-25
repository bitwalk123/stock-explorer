from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QWidget

from funcs.tbl_currency import get_dict_id_currency
from ui.dock_items import DockItems
from widgets.areas import ScrollAreaVertical, Container
from widgets.buttons import TickerButton
from widgets.labels import DockImgTitle
from widgets.layouts import VBoxLayout, HBoxLayout
from widgets.pads import VPad
from widgets.tab_panels import TabPanelMain


class DockExchange(DockItems):
    tickerSelected = Signal(str)
    defaultCurrency = 'USDJPY'

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.vbox: VBoxLayout = None
        self.tb_group: QButtonGroup = None

        self.dict_id_currency = get_dict_id_currency()
        self.list_id_currency = [
            self.dict_id_currency[currency] for currency in self.dict_id_currency.keys()
        ]
        self.dict_tb = dict()

        self.init_ui()

    def init_ui(self):
        # Dock Title
        title = DockImgTitle('ticker.png', '為替')
        self.setTitleBarWidget(title)

        area = ScrollAreaVertical()
        self.setWidget(area)

        base = Container()
        area.setWidget(base)

        self.vbox = vbox = VBoxLayout()
        self.gen_currency_buttons(vbox)
        vbox.addWidget(VPad())
        base.setLayout(vbox)

    def gen_currency_buttons(self, vbox):
        self.tb_group = tb_group = QButtonGroup(self)
        for currency in self.dict_id_currency.keys():
            tb = TickerButton(currency)
            id_currency = self.dict_id_currency[currency]
            self.dict_tb[id_currency] = tb

            if currency != self.defaultCurrency:
                tb.setEnabled(False)

            tb_group.addButton(tb)
            tb_group.setId(tb, id_currency)
            vbox.addWidget(tb)
        tb_group.buttonClicked.connect(self.on_button_clicked)

    def getCurrentCurrency(self) -> Union[str, None]:
        tb = self.tb_group.checkedButton()
        if tb is not None:
            return tb.text()
        else:
            return None

    def getCurrentDefault(self) -> str:
        return self.defaultCurrency

    def on_button_clicked(self, tb: TickerButton):
        if tb.isChecked():
            self.setTickerButtonVisible(tb)
            code = tb.text()
            self.tickerSelected.emit(code)

    def setCheck(self, currency: str):
        id_currency = self.dict_id_currency[currency]
        if id_currency != self.tb_group.checkedId():
            tb: Union[QWidget, TickerButton] = self.dict_tb[id_currency]
            tb.setChecked(True)
            self.setTickerButtonVisible(tb)

    def setTickerButtonVisible(self, tb: Union[QWidget, TickerButton]):
        area: Union[QWidget, ScrollAreaVertical] = self.widget()
        area.ensureWidgetVisible(tb)
