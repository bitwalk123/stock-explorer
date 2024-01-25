from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QWidget

from funcs.tbl_iticker import get_dict_id_index
from ui.dock_items import DockItems
from widgets.areas import ScrollAreaVertical, Container
from widgets.buttons import TickerButton, IndexButton
from widgets.labels import DockImgTitle
from widgets.layouts import VBoxLayout, HBoxLayout
from widgets.pads import VPad
from widgets.tab_panels import TabPanelMain


class DockIndices(DockItems):
    tickerSelected = Signal(str)
    defaultIndex = '^N255'

    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        self.vbox: VBoxLayout | None = None
        self.tb_group: QButtonGroup | None = None

        self.dict_id_index = get_dict_id_index()
        self.list_id_index = [
            self.dict_id_index[iticker] for iticker in self.dict_id_index.keys()
        ]
        self.dict_tb = dict()

        self.init_ui()

    def init_ui(self):
        # Dock Title
        title = DockImgTitle('ticker.png', '指数')
        self.setTitleBarWidget(title)

        area = ScrollAreaVertical()
        self.setWidget(area)

        base = Container()
        area.setWidget(base)

        self.vbox = vbox = VBoxLayout()
        self.gen_index_buttons(vbox)
        vbox.addWidget(VPad())
        base.setLayout(vbox)

    def gen_index_buttons(self, vbox):
        self.tb_group = tb_group = QButtonGroup(self)
        for iticker in self.dict_id_index.keys():
            ib = IndexButton(iticker)
            id_index = self.dict_id_index[iticker]
            self.dict_tb[id_index] = ib
            tb_group.addButton(ib)
            tb_group.setId(ib, id_index)
            vbox.addWidget(ib)
        tb_group.buttonClicked.connect(self.on_button_clicked)

    def getCurrentIndex(self) -> Union[str, None]:
        ib: IndexButton = self.tb_group.checkedButton()
        if ib is not None:
            return ib.getText()
        else:
            return None

    def getCurrentDefault(self) -> str:
        return self.defaultIndex

    def on_button_clicked(self, ib: IndexButton):
        if ib.isChecked():
            self.setTickerButtonVisible(ib)
            code = ib.text()
            self.tickerSelected.emit(code)

    def setCheck(self, iticker: str):
        id_index = self.dict_id_index[iticker]
        if id_index != self.tb_group.checkedId():
            tb: Union[QWidget, TickerButton] = self.dict_tb[id_index]
            tb.setChecked(True)
            self.setTickerButtonVisible(tb)

    def setTickerButtonVisible(self, tb: Union[QWidget, TickerButton]):
        area: Union[QWidget, ScrollAreaVertical] = self.widget()
        area.ensureWidgetVisible(tb)
