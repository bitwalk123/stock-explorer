import os
import pandas as pd
import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QApplication, QMainWindow

from funcs.tbl_ticker import get_dict_id_code
from snippets.set_env import set_env
from sqls.sql_trade_day import (
    sql_ins_into_trade1m_values,
    sql_sel_id_trade1m_from_trade1m_with_datetime_id_code,
    sql_upd_trade1m_values,
)
from structs.db_info import DBInfo
from ui.toolbar_dta import DTAUploaderToolBar


class DTAUploader1m(QMainWindow):
    def __init__(self):
        super().__init__()
        dict_info = set_env()
        self.dir = 'cache'
        # _____________________________________________________________________
        # Top Toolbar
        self.toolbar = toolbar = DTAUploaderToolBar()
        toolbar.clickedStart.connect(self.start_upload)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def start_upload(self):
        dict_id_code = get_dict_id_code()

        pattern = re.compile(r'.+/([0-9]{4})\.T_[0-9]{4}-[0-9]{2}-[0-9]{2}_.+_1m\.pkl$')
        list_file = [
            os.path.join(self.dir, f) for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))
        ]
        list_file.sort()

        con = DBInfo.get_connection()
        if con.open():
            for file in list_file:
                m = pattern.match(file)
                if not m:
                    continue

                print(file)
                code = m.group(1)
                id_code = dict_id_code[code]
                # print(id_code)
                df = pd.read_pickle(file)
                # print(df)

                for row in df.index:
                    timestamp = int(row.timestamp())
                    series = df.loc[row].copy()
                    series['Datetime'] = timestamp
                    # print(series)
                    # print(row)
                    query = QSqlQuery()
                    sql = sql_sel_id_trade1m_from_trade1m_with_datetime_id_code(id_code, timestamp)
                    query.exec(sql)
                    if query.next():
                        id_trade = query.value(0)
                        sql = sql_upd_trade1m_values(id_trade, series)
                    else:
                        sql = sql_ins_into_trade1m_values(id_code, series)
                    if not query.exec(sql):
                        print(query.lastError())
            con.close()
            print('Completed!')
            return True
        else:
            print('database can not be opened!')
            return False


def main():
    app = QApplication()
    ex = DTAUploader1m()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
