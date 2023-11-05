import pandas as pd
from PySide6.QtSql import QSqlQuery

from PySide6.QtWidgets import QVBoxLayout

from database.sqls_predict import select_max_date_from_predict
from functions.conv_timestamp2date import conv_timestamp2date
from functions.resources import get_connection
from ui_modules.panel_abstract import TabPanelAbstract


class TabPanelPredictions(TabPanelAbstract):
    tab_label = '始値予測一覧'

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        con = get_connection()
        if con.open():
            sql = select_max_date_from_predict()
            query = QSqlQuery(sql)
            if query.next():
                date_int = query.value(0)
                print(date_int, conv_timestamp2date(date_int))
            con.close()
