from PySide6.QtCore import Qt

from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from functions.get_predict_date import get_predict_date_latest
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.labels import LabelDate, LabelFlat
from widgets.widgets import HPad


class TabPanelPredictions(TabPanelAbstract):
    tab_label = '始値予測一覧'

    def __init__(self):
        super().__init__()
        # self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        bar = QWidget()
        # bar.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(bar)

        layout2 = QHBoxLayout()
        layout2.setSpacing(0)
        layout2.setContentsMargins(0, 0, 0, 0)
        bar.setLayout(layout2)

        lab_date_title = LabelFlat("Prediction Date")
        layout2.addWidget(lab_date_title)
        lab_date = LabelDate()
        date_predict = get_predict_date_latest()
        lab_date.setDate(date_predict)
        lab_date.setFixedWidth(100)
        layout2.addWidget(lab_date)
        pad = HPad()
        layout2.addWidget(pad)
