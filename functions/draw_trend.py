import mplfinance as mpf
from PySide6.QtSql import QSqlQuery

from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dict_code import get_dict_code, get_dict_id_code
from functions.get_open_with_code import get_open_with_code
from functions.get_trade_with_code import get_trade_with_code
from functions.resources import get_connection
from widgets.charts import Trend


def draw_trend(chart: Trend, code: int = 0, start: int = -1, gtype: str = 'Open'):
    """Draw trend chart with specified ticker code

    Args:
        chart (Trend): instance of Trend
        start (int): start date in UNIX epoch sec
        code (int): ticker code
        gtype (str): graph type
    """
    if gtype == 'Open':
        draw_trend_open(chart, code, start)
    elif gtype == 'Candle':
        draw_trend_candle(chart, code, start)
    else:
        print('not support plot type: %s' % gtype)


def draw_trend_open(chart: Trend, code: int, start: int):
    """Draw trend chart for Open with specified ticker code

    Args:
        chart (Trend): instance of Trend
        code (int): ticker code
        start (int): start date in UNIX epoch sec
    """
    if code > 0:
        cname, list_x, list_y, list_z = get_open_with_code(code, start)
    else:
        cname = None
        list_x = list()
        list_y = list()
        list_z = list()

    chart.clearAxes()
    #
    if code > 0:
        chart.ax1.set_title('%s (%d.T) Open' % (cname, code))

    chart.ax1.plot(list_x, list_y)
    chart.ax2.bar(list_x, list_z)

    chart.ax1.set_ylabel('Price')
    chart.ax2.set_ylabel('Volume')

    chart.ax1.grid()
    chart.ax2.grid()
    for tick1, tick2 in zip(chart.ax1.get_xticklabels(), chart.ax2.get_xticklabels()):
        tick1.set_rotation(90)
        tick2.set_rotation(45)
    #
    chart.refreshDraw()

    con = get_connection()
    if con.open():
        dict_id_code = get_dict_id_code()
        sql = 'SELECT lastSplitDate FROM split WHERE id_code=%d' % dict_id_code[code]
        query = QSqlQuery(sql)
        last_split_date = 0
        while query.next():
            last_split_date = query.value(0)
        con.close

        #print(dict_id_code[code], code, last_split_date)
        if last_split_date > 0:
            print(code, ': split on', conv_timestamp2date(last_split_date), 'id_code =', dict_id_code[code])


def draw_trend_candle(chart: Trend, code: int, start: int):
    """Draw trend chart for Open with specified ticker code

    Args:
        chart (Trend): instance of Trend
        code (int): ticker code
        start (int): start date in UNIX epoch sec
    """
    cname, df = get_trade_with_code(code, start)
    chart.clearAxes()
    # title
    chart.ax1.set_title('%s (%d.T)' % (cname, code))

    # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
    mpf.plot(
        df,
        type='candle',
        datetime_format='%Y/%m/%d',
        tight_layout=False,
        style='binance',
        mav=(21, 42),
        ax=chart.ax1,
        volume=chart.ax2
    )
    #
    chart.ax1.grid()
    chart.ax2.grid()
    chart.refreshDraw()
