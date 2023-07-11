#!/usr/bin/env python
# coding: utf-8
import random
import sys

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from functions.resources import get_ini_file, get_connection
from ui_modules.dock_ticker import DockTicker
from ui_modules.toolbars import ToolBarMain
from ui_modules.win_canvas import MplCanvas


class StockExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')

        self.plot = None

        # ini ファイル（フルパス）
        self.file_ini = get_ini_file()
        print(self.file_ini)

        # self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        # ツールバー
        toolbar = ToolBarMain()
        self.addToolBar(toolbar)
        # コードドック
        dock_left = DockTicker()
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)

        self.plot = MplCanvas()
        self.draw_plot()
        self.setCentralWidget(self.plot)

    def draw_plot(self):
        # TEST PLOTS
        # n_data = 100
        # list_x = [x for x in range(n_data)]
        # list_y = [(random.random() - 0.5) * 100 for i in range(n_data)]
        code, cname, list_x, list_y = self.get_sample_data()
        self.plot.axes.plot(list_x, list_y)
        #
        self.plot.axes.set_title('%s (%d.T)' % (cname, code))
        self.plot.axes.set_xlabel('日付')
        self.plot.axes.set_ylabel('株価')
        self.plot.axes.grid()

    def get_sample_data(self):
        code = 5217
        list_x = list()
        list_y = list()
        con = get_connection()
        if con.open():
            id_ticker = 0
            sql = 'select id_ticker, 銘柄名 from ticker where コード=%d;' % code
            query = QSqlQuery(sql)
            while query.next():
                id_ticker = query.value(0)
                cname = query.value(1)
                print(id_ticker)
                break

            sql = 'SELECT date, open FROM trade WHERE id_code=%d ORDER BY date;' % id_ticker
            query = QSqlQuery(sql)
            while query.next():
                list_x.append(query.value(0))
                list_y.append(query.value(1))

            con.close()

        return code, cname, list_x, list_y

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        print('アプリケーションを終了します。')
        event.accept()  # let the window close


def main():
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
