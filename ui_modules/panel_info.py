from PySide6.QtWidgets import (
    QHBoxLayout,
    QSizePolicy,
    QWidget,
)

from functions.get_volume_median_with_code_start import get_volume_median_with_code_start
from widgets.labels import (
    LabelFlat,
    LabelTitle,
    LabelValue,
)


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

        title_volume = LabelTitle('Volume(median)')
        layout.addWidget(title_volume)

        self.disp_volume = LabelValue()
        layout.addWidget(self.disp_volume)

        # 余白のスペーサ
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(hpad)

    def update_ticker(self, code: int, start: int):
        self.disp_code.setText('%d.T' % code)
        volume_median = get_volume_median_with_code_start(code, start)
        self.disp_volume.setText('%d' % volume_median)