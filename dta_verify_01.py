import numpy as np
import os
import pandas as pd
import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow, QWidget,
)
from scipy.interpolate import make_smoothing_spline

from funcs.dta_funcs import dta_prep_candle1m
from structs.param import ParamSmoothing
from ui.toolbar_dta import DTAVerifyToolBar
from widgets.charts import ChartForVerify01


class DTAVerify(QMainWindow):
    def __init__(self):
        super().__init__()
        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAVerifyToolBar()
        toolbar.clickedStart.connect(self.start_verification)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartForVerify01()
        self.setCentralWidget(chart)

    def start_verification(self):
        ticker = '8035'
        list_filename = self.get_filelist(ticker)
        # print(list_filename)

        ts_list = list()
        x1_list = list()
        x2_list = list()
        x3_list = list()
        pattern = re.compile(r'.+/%s.*_([0-9]{4}-[0-9]{2}-[0-9]{2})_.+_1m\.pkl$' % ticker)
        for filename in list_filename:
            m = pattern.match(filename)
            if m:
                ts_str = m.group(1)
                # print(filename, ts_str)
                df = pd.read_pickle(filename)
                # print(df)
                x_array, y_array = dta_prep_candle1m(ts_str, df)
                # print(x_array)
                # print(y_array)
                y_mean = np.mean(y_array)
                std = np.std(y_array)
                y_scaled = np.array([(y - y_mean) / std for y in y_array])
                # _____________________________________________________________________
                # Smoothing Spline
                param = ParamSmoothing()
                t_start = param.start
                t_end = param.end
                t_interval = param.interval
                lam = param.lam
                spl = make_smoothing_spline(x_array, y_scaled, lam=lam)
                xs = np.linspace(t_start, t_end, int((t_end - t_start) / t_interval))
                ys = spl(xs)
                # _____________________________________________________________________
                # Integrals for Morning and Afternoon
                count = 0
                sum_morning = 0
                sum_afternoon = 0
                noon = 0
                for h in ys:
                    if count == int(t_end / 2):
                        noon = h
                    elif count < t_end / 2:
                        sum_morning += h
                    else:
                        sum_afternoon += h
                    count += 1
                # print('%s : (%d, %d)' % (ts_str, round(sum_morning), round(sum_afternoon)))
                ts_list.append(ts_str)
                x1_list.append(sum_morning)
                x2_list.append(sum_afternoon)
                x3_list.append(noon)

        df0 = pd.DataFrame({
            'ts': ts_list,
            'morning': x1_list,
            'afternoon': x2_list,
            'noon': x3_list,
        })
        df0['ts'] = pd.to_datetime(df0['ts'])
        df1 = df0.set_index('ts')
        print(df1)

        chart: QWidget | ChartForVerify01 = self.centralWidget()
        chart.clearAxes()

        chart.ax1.plot(df1.index, df1['noon'], lw=1, c='C0')
        chart.ax1.scatter(df1.index, df1['noon'], s=10, c='C0')

        chart.ax1.axhline(y=0, linestyle='solid', lw=0.75, c='black')
        chart.ax1.axhline(y=np.mean(df1['noon']), linestyle='dashed', lw=1, c='red')

        chart.ax1.grid()

        chart.ax2.bar(x=df1.index, height=df1['morning'], color='C0')
        chart.ax2.bar(x=df1.index, height=df1['afternoon'], color='C1')

        chart.ax2.axhline(y=0, linestyle='solid', lw=0.75, c='black')

        chart.ax2.grid()

        chart.refreshDraw()

    def get_filelist(self, ticker: str):
        dir_path = 'cache'
        pattern = re.compile(r'%s/%s.+\.pkl$' % (dir_path, ticker))
        # print(pattern)
        list_file = [
            os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
        ]
        # print(list_file)
        list_target = list()
        for f in list_file:
            if pattern.match(f):
                list_target.append(f)
        list_target.sort()
        # print(list_target)

        # list_target = [list_target[0]]
        return list_target


def main():
    app = QApplication()
    ex = DTAVerify()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
