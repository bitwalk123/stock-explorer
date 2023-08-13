import mplfinance as mpf

from functions.get_open_with_code import get_open_with_code
from functions.get_trade_with_code import get_trade_with_code
from ui_modules.charts import Trend


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
        cname, list_x, list_y = get_open_with_code(code, start)
    else:
        cname = None
        list_x = list()
        list_y = list()

    chart.clearAxes()
    #
    chart.ax.plot(list_x, list_y)
    if code > 0:
        chart.ax.set_title('%s (%d.T) Open' % (cname, code))
    # chart.axes.set_xlabel('DATE')
    chart.ax.set_ylabel('Price')
    chart.ax.grid()
    for tick in chart.ax.get_xticklabels():
        tick.set_rotation(45)
    #
    chart.refreshDraw()


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
    chart.ax.set_title('%s (%d.T)' % (cname, code))

    # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
    mc = mpf.make_marketcolors(
        up='cyan',
        down='orange',
        wick={'up': 'blue', 'down': 'red'},
    )
    s = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(
        df,
        type='candle',
        datetime_format='%Y/%m/%d',
        tight_layout=False,
        style=s,
        mav=(21, 42),
        ax=chart.ax
    )
    #
    chart.ax.grid()
    chart.refreshDraw()
