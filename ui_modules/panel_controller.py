from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)

from functions.get_volume_median import get_volume_median_with_code_start
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelTitle,
    LabelValue,
)
from widgets.widgets import HPad


class PanelInfo(QWidget):

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title_index = LabelFlat('Indices')
        layout.addWidget(title_index)

        title_code = LabelTitle('Code')
        layout.addWidget(title_code)

        self.disp_code = LabelValue()
        layout.addWidget(self.disp_code)

        title_from = LabelTitle('From')
        layout.addWidget(title_from)

        self.disp_from = LabelDate()
        layout.addWidget(self.disp_from)

        title_to = LabelTitle('To')
        layout.addWidget(title_to)

        self.disp_to = LabelDate()
        layout.addWidget(self.disp_to)

        title_num = LabelTitle('N')
        layout.addWidget(title_num)

        self.disp_num = LabelValue()
        layout.addWidget(self.disp_num)

        title_volume = LabelTitle('Volume(median)')
        layout.addWidget(title_volume)

        self.disp_volume = LabelValue()
        layout.addWidget(self.disp_volume)

        hpad = HPad()
        layout.addWidget(hpad)

    def update_ticker(self, code: int, start: int):
        self.disp_code.setText('%d' % code)
        date_min, date_max, volume_median, num = get_volume_median_with_code_start(code, start)
        self.disp_from.setDate(date_min)
        self.disp_to.setDate(date_max)
        self.disp_volume.setText(format(volume_median, ','))
        self.disp_num.setText('%d' % num)
