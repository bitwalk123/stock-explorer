from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QWidget,
)

from funcs.tbl_ticker import get_dict_id_code
from ui.dock_items import DockItems
from widgets.tab_panels import TabPanelMain
from widgets.areas import (
    Container,
    ScrollAreaVertical,
)
from widgets.buttons import TickerButton
from widgets.labels import DockImgTitle
from widgets.layouts import HBoxLayout, VBoxLayout
from widgets.pads import VPad


class DockDomesticTickers(DockItems):
    tickerSelected = Signal(str)

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.vbox: VBoxLayout = None
        self.tb_group: QButtonGroup = None

        self.dict_id_code = get_dict_id_code()
        self.list_id_code = [
            self.dict_id_code[code] for code in self.dict_id_code.keys()
        ]
        self.dict_tb = dict()
        self.init_ui()

    def init_ui(self):
        # Dock Title
        title = DockImgTitle('ticker.png', 'コード')
        self.setTitleBarWidget(title)

        area = ScrollAreaVertical()
        self.setWidget(area)

        base = Container()
        area.setWidget(base)

        hbox = HBoxLayout()
        base.setLayout(hbox)

        self.vbox = vbox = VBoxLayout()
        self.gen_ticker_buttons(vbox)
        hbox.addLayout(vbox)

        pad = VPad()
        pad.setFixedWidth(16)
        hbox.addWidget(pad)

    def gen_ticker_buttons(self, vbox):
        self.tb_group = tb_group = QButtonGroup(self)
        for code in self.dict_id_code.keys():
            tb = TickerButton(code)
            id_code = self.dict_id_code[code]
            self.dict_tb[id_code] = tb
            tb_group.addButton(tb)
            tb_group.setId(tb, id_code)
            vbox.addWidget(tb)
        tb_group.buttonClicked.connect(self.on_button_clicked)

    def getCurrentTicker(self) -> Union[str, None]:
        tb = self.tb_group.checkedButton()
        if tb is not None:
            return tb.text()
        else:
            return None

    def getIdCode(self, code: str) -> int:
        return self.dict_id_code[code]

    def getTickerFirst(self) -> str:
        tb: Union[QWidget, TickerButton] = self.vbox.itemAt(0).widget()
        code = tb.text()
        return code

    def setCheck(self, code: str):
        id_code = self.dict_id_code[code]
        if id_code != self.tb_group.checkedId():
            tb: Union[QWidget, TickerButton] = self.dict_tb[id_code]
            tb.setChecked(True)
            self.setTickerButtonVisible(tb)

    def on_button_clicked(self, tb: TickerButton):
        if tb.isChecked():
            self.setTickerButtonVisible(tb)
            code = tb.text()
            self.tickerSelected.emit(code)

    def set_tb_checked_with_id(self, id_code: int):
        if id_code in self.list_id_code:
            tb = self.tb_group.button(id_code)
            tb.setChecked(True)
            self.setTickerButtonVisible(tb)

    def set_ticker(self, id_code) -> str:
        self.set_tb_checked_with_id(id_code)
        # Get checked instance to get code
        tb = self.tb_group.checkedButton()
        return tb.text()

    def setTickerButtonVisible(self, tb: Union[QWidget, TickerButton]):
        area: Union[QWidget, ScrollAreaVertical] = self.widget()
        area.ensureWidgetVisible(tb)

    def setTickerDown(self) -> str:
        id_code = self.tb_group.checkedId()
        id_code_new = id_code + 1
        return self.set_ticker(id_code_new)

    def setTickerUp(self) -> str:
        id_code = self.tb_group.checkedId()
        id_code_new = id_code - 1
        return self.set_ticker(id_code_new)

    def updateTicker(self, code: str) -> bool:
        if code in self.dict_id_code.keys():
            id_code = self.dict_id_code[code]
            tb: TickerButton = self.tb_group.button(id_code)
            tb.setChecked(True)
            self.setTickerButtonVisible(tb)
            return True
        else:
            return False
