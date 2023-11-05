from PySide6.QtCore import Qt

from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from functions.get_predict import (
    get_predict_dataframe,
    get_predict_date_latest,
)
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.labels import LabelDate, LabelFlat
from widgets.widgets import HPad


class TabPanelPredict(TabPanelAbstract):
    tab_label = '始値予測一覧'

    def __init__(self):
        super().__init__()
        # self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setLayout(layout)

        bar = QWidget()
        layout.addWidget(bar)

        layout_bar = QHBoxLayout()
        layout_bar.setSpacing(0)
        layout_bar.setContentsMargins(0, 0, 0, 0)
        bar.setLayout(layout_bar)

        lab_date_title = LabelFlat('Target Date')
        layout_bar.addWidget(lab_date_title)
        lab_date = LabelDate()
        date_predict = get_predict_date_latest()
        lab_date.setDate(date_predict)
        lab_date.setFixedWidth(100)
        layout_bar.addWidget(lab_date)
        pad = HPad()
        layout_bar.addWidget(pad)

        df_pred = get_predict_dataframe(date_predict)
        print(df_pred)
