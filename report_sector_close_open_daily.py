import sys
import time

from PySide6.QtWidgets import QApplication
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

from funcs.tbl_trade_diff import diff_close_by_sector, diff_close_open_by_sector
from funcs.tide import (
    conv_timestamp2date,
    conv_timestamp2year,
    get_elapsed,
    get_latest_date,
)
from snippets.set_env import set_env

FONT_PATH = r'fonts/RictyDiminished-Regular.ttf'
loc_report = '/home/bitwalk/MyProjects/stock/report/%d/'


def report_sector_close_open_diff():
    latest_date = get_latest_date()
    date_report = str(conv_timestamp2date(latest_date))
    print('Generating close - open repoty for %s...' % date_report)
    sector_delta = diff_close_open_by_sector(latest_date)
    fp_title = FontProperties(fname=FONT_PATH, size=16)
    fp_axlabel = FontProperties(fname=FONT_PATH, size=14)
    fp_tick = FontProperties(fname=FONT_PATH, size=11)
    list_sector = list()
    list_data = list()
    for sector in sector_delta.get_sectors():
        list_sector.append(sector)
        list_data.append(sector_delta.get_dist_raw(sector))
    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.boxplot(
        list_data,
        labels=list_sector,
        vert=False,
        flierprops={'marker': 'o', 'markersize': 1.5}
    )
    for label in ax.get_yticklabels():
        label.set_fontproperties(fp_tick)
    ax.set_xlabel('差分（円）', fontproperties=fp_axlabel)
    ax.set_xlim(-200, 200)
    ax.set_ylabel('33業種区分', fontproperties=fp_axlabel)
    plt.title('%s 東証 終値 - 始値' % date_report, fontproperties=fp_title)
    plt.grid()
    plt.subplots_adjust(left=0.35, right=0.95, bottom=0.1, top=0.9)
    year = conv_timestamp2year(latest_date)
    plt.savefig('%s/close_open_%d.png' % (loc_report % year, latest_date))
    # plt.show()


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    dict_info = set_env()
    time_start = time.time()

    report_sector_close_open_diff()
    print('elapsed %.3f sec' % get_elapsed(time_start))
