from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

from functions.conv_timestamp2date import conv_timestamp2date
from functions.diff_close import diff_close_by_sector
from functions.get_latest_2dates import get_latest_2dates

if __name__ == '__main__':
    pair_date = get_latest_2dates()
    date_report = str(conv_timestamp2date(pair_date[1]))
    print(date_report)
    sector_delta = diff_close_by_sector(pair_date)

    fp_title = FontProperties(fname=r'fonts/RictyDiminished-Regular.ttf', size=16)
    fp_axlabel = FontProperties(fname=r'fonts/RictyDiminished-Regular.ttf', size=14)
    fp_tick = FontProperties(fname=r'fonts/RictyDiminished-Regular.ttf', size=11)

    list_sector = list()
    list_data = list()
    for sector in sector_delta.get_sectors():
        list_sector.append(sector)
        list_data.append(sector_delta.get_dist_raw(sector))
        # list_data.append(sector_delta.get_dist_standardize(sector))

    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.boxplot(
        list_data,
        labels=list_sector,
        vert=False,
        flierprops={'marker': 'o', 'markersize': 2}
    )

    for label in ax.get_yticklabels():
        label.set_fontproperties(fp_tick)

    ax.set_xlabel('差分（円）', fontproperties=fp_axlabel)
    ax.set_ylabel('33業種区分', fontproperties=fp_axlabel)
    plt.title('%s 東証終値の前日差' % date_report, fontproperties=fp_title)
    plt.grid()

    plt.subplots_adjust(left=0.35, right=0.95, bottom=0.1, top=0.9)

    plt.savefig('pool/close_%d.png' % pair_date[1])
    # plt.show()
