from PySide6.QtWidgets import QStatusBar

from structs.trend_object import TrendObj
from widgets.areas import Container
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelTitle,
    LabelValue,
)
from widgets.layouts import HBoxLayout
from widgets.tab_panels import TabPanelMain


class StatusbarDomesticTicker(QStatusBar):
    def __init__(self, parent: TabPanelMain):
        super().__init__(parent)
        base = Container()
        self.addWidget(base)

        layout = HBoxLayout()
        base.setLayout(layout)
        # _____________________________________________________________________
        # Indices (title)
        title_index = LabelFlat('情報')
        layout.addWidget(title_index)
        # _____________________________________________________________________
        # Code
        title_code = LabelTitle('Code')
        layout.addWidget(title_code)
        self.disp_code = LabelValue()
        layout.addWidget(self.disp_code)
        # _____________________________________________________________________
        # 33業種区分
        title_13sector = LabelTitle('33業種区分')
        layout.addWidget(title_13sector)
        self.disp_13sector = LabelValue()
        layout.addWidget(self.disp_13sector)
        # _____________________________________________________________________
        # From
        title_from = LabelTitle('From')
        layout.addWidget(title_from)
        self.disp_from = LabelDate()
        layout.addWidget(self.disp_from)
        # _____________________________________________________________________
        # To
        title_to = LabelTitle('To')
        layout.addWidget(title_to)
        self.disp_to = LabelDate()
        layout.addWidget(self.disp_to)
        # _____________________________________________________________________
        # N
        title_num = LabelTitle('N')
        layout.addWidget(title_num)
        self.disp_num = LabelValue()
        layout.addWidget(self.disp_num)
        # _____________________________________________________________________
        # Volume
        title_volume = LabelTitle('Volume(median)')
        layout.addWidget(title_volume)
        self.disp_volume = LabelValue()
        layout.addWidget(self.disp_volume)

    def updateTicker(self, obj: TrendObj):
        self.disp_code.setValue(obj.getCode())
        self.disp_13sector.setValue(obj.get13Sector())
        self.disp_from.setValue(obj.getDateFrom())
        self.disp_to.setValue(obj.getDateTo())
        self.disp_num.setValue(obj.getNum())
        self.disp_volume.setValue(obj.getVolume())

