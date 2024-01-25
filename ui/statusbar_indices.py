from PySide6.QtWidgets import QStatusBar

from structs.trend_object import TrendObj
from widgets.areas import Container
from widgets.labels import LabelFlat, LabelTitle, LabelValue, LabelDate
from widgets.layouts import HBoxLayout
from widgets.tab_panels import TabPanelMain


class StatusbarIndices(QStatusBar):
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
        title_index = LabelTitle('Index')
        layout.addWidget(title_index)
        self.disp_index = LabelValue()
        layout.addWidget(self.disp_index)
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

    def updateIndices(self, obj: TrendObj):
        self.disp_index.setValue(obj.getCode())
        self.disp_from.setValue(obj.getDateFrom())
        self.disp_to.setValue(obj.getDateTo())
        self.disp_num.setValue(obj.getNum())
