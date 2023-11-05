import pandas as pd

from PySide6.QtWidgets import QLabel, QFileDialog, QVBoxLayout

from functions.read_csv import read_csv_contract_from_shiftjis
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.buttons import ButtonIcon
from widgets.layout import GridLayout


class TabPanelPredictions(TabPanelAbstract):
    tab_label = '始値予測一覧'

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
