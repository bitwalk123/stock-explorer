import mplfinance as mpf

from funcs.tbl_exchange import get_trend_object_exchange
from funcs.tbl_trade import (
    get_trend_object_candle,
    get_trend_object_close,
    get_trend_object_close_open,
    get_trend_object_open,
)
from structs.res import AppRes
from structs.trend_object import TrendObj
from widgets.charts import ChartAbstract, Trend


def draw_chart(
        chart: ChartAbstract,
        code: str,
        start: int = -1,
        gtype: str = 'Candle'
) -> TrendObj:
    """Draw trend chart with specified ticker code

    Args:
        chart (Trend): instance of Trend
        start (int): start date in UNIX epoch sec
        code (str): ticker code
        gtype (str): graph type
    Returns:
        TrendObj
    """
    if gtype == 'Candle':
        obj = draw_candle_stick(chart, code, start)
    elif gtype == 'Open':
        obj = draw_open(chart, code, start)
    elif gtype == 'Close':
        obj = draw_close(chart, code, start)
    elif gtype == 'Close - Open':
        obj = draw_close_open(chart, code, start)
    elif gtype == 'exchange':
        obj = draw_exchange(chart, code, start)
    else:
        obj = None
        print('not support plot type: %s' % gtype)

    return obj


def draw_candle_stick(chart: Trend, code: str, start: int = -1) -> TrendObj:
    """Draw trend chart with specified ticker code

    Args:
        chart (Trend): instance of Trend
        start (int): start date in UNIX epoch sec
        code (str): ticker code
    Returns:
        TrendObj
    """
    res = AppRes()
    obj = get_trend_object_candle(code, start)
    cname = obj.getCname()
    df = obj.getDataFrame()

    if chart.getType() == 'Candle':
        chart.clearAxes()
    else:
        chart.removeAxes()
        chart.initCandleStick()

    chart.ax.tick_params(axis='x', labelsize=12)
    chart.ax2.tick_params(axis='x', labelsize=12)

    # title
    chart.ax.set_title('%s (%s)' % (cname, code))
    # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
    mpf.plot(
        df,
        type='candle',
        datetime_format='%y/%m/%d',
        tight_layout=False,
        style=res.getCandleStyle(),
        mav=(5, 25),
        ax=chart.ax,
        volume=chart.ax2
    )
    # chart.ax.yaxis.tick_right()
    # chart.ax2.yaxis.tick_right()
    # chart.ax.yaxis.set_label_position('right')
    # chart.ax2.yaxis.set_label_position('right')
    chart.ax.yaxis.set_tick_params(labelright=True)
    chart.ax2.yaxis.set_tick_params(labelright=True)

    chart.ax.grid()
    chart.ax2.grid()
    chart.refreshDraw()

    return obj


def draw_open(chart: Trend, code: str, start: int = -1) -> TrendObj:
    obj = get_trend_object_open(code, start)
    cname = obj.getCname()
    df = obj.getDataFrame()

    if chart.getType() == 'Trend':
        chart.clearAxes()
    else:
        chart.removeAxes()
        chart.initTrend()

    chart.ax.tick_params(axis='x', labelsize=12)

    # title
    chart.ax.set_title('%s - Open (%s)' % (cname, code))
    chart.ax.plot(
        df.index,
        df['Open'],
        color='darkolivegreen',
        marker='o',
        markersize=4,
        linewidth=0.5
    )
    # chart.ax.yaxis.tick_right()
    # chart.ax.yaxis.set_label_position('right')
    chart.ax.yaxis.set_tick_params(labelright=True)
    chart.ax.set_ylabel('Price')
    for tick in chart.ax.get_xticklabels():
        tick.set_rotation(45)
    chart.ax.grid()
    chart.refreshDraw()

    return obj


def draw_close(chart: Trend, code: str, start: int = -1) -> TrendObj:
    obj = get_trend_object_close(code, start)
    cname = obj.getCname()
    df = obj.getDataFrame()

    if chart.getType() == 'Trend':
        chart.clearAxes()
    else:
        chart.removeAxes()
        chart.initTrend()

    chart.ax.tick_params(axis='x', labelsize=12)

    # title
    chart.ax.set_title('%s - Close (%s)' % (cname, code))
    chart.ax.plot(
        df.index,
        df['Close'],
        color='maroon',
        marker='o',
        markersize=4,
        linewidth=0.5
    )
    # chart.ax.yaxis.tick_right()
    # chart.ax.yaxis.set_label_position('right')
    chart.ax.yaxis.set_tick_params(labelright=True)
    chart.ax.set_ylabel('Price')
    for tick in chart.ax.get_xticklabels():
        tick.set_rotation(45)
    chart.ax.grid()
    chart.refreshDraw()

    return obj


def draw_close_open(chart: Trend, code: str, start: int = -1) -> TrendObj:
    obj = get_trend_object_close_open(code, start)
    cname = obj.getCname()
    df = obj.getDataFrame()

    if chart.getType() == 'Trend':
        chart.clearAxes()
    else:
        chart.removeAxes()
        chart.initTrend()

    chart.ax.tick_params(axis='x', labelsize=12)

    # title
    chart.ax.set_title('%s - (Close - Open) (%s)' % (cname, code))

    # Reference:
    # https://stackoverflow.com/questions/18973404/how-to-change-the-color-of-a-single-bar-in-a-bar-plot
    chart.ax.bar(
        df.index,
        df['Delta']
    )
    for i, delta in enumerate(df['Delta']):
        if delta > 0:
            color = 'dodgerblue'
        elif delta < 0:
            color = 'salmon'
        else:
            color = 'gray'
        chart.ax.get_children()[i].set_color(color)

    # chart.ax.yaxis.tick_right()
    # chart.ax.yaxis.set_label_position('right')
    chart.ax.yaxis.set_tick_params(labelright=True)
    chart.ax.set_ylabel('Price')
    for tick in chart.ax.get_xticklabels():
        tick.set_rotation(45)
    chart.ax.grid()

    chart.refreshDraw()

    return obj


def draw_exchange(chart: Trend, currency: str, start: int = -1) -> TrendObj:
    res = AppRes()
    obj = get_trend_object_exchange(currency, start)
    df = obj.getDataFrame()

    if chart.getType() == 'Trend':
        chart.clearAxes()
    else:
        chart.removeAxes()
        chart.initTrend()

    chart.ax.tick_params(axis='x', labelsize=12)

    # title
    title_currency = gen_title_exchange(currency)
    chart.ax.set_title(title_currency)
    mpf.plot(
        df,
        type='candle',
        datetime_format='%y/%m/%d',
        tight_layout=False,
        style=res.getCandleStyle(),
        mav=(5, 25),
        ax=chart.ax
    )
    chart.ax.set_ylabel('Price (JPY)')
    # chart.ax.yaxis.tick_right()
    # chart.ax.yaxis.set_label_position('right')
    chart.ax.yaxis.set_tick_params(labelright=True)
    chart.ax.grid()
    chart.refreshDraw()

    return obj


def gen_title_exchange(currency: str) -> str:
    if len(currency) != 6:
        return currency
    currency1 = currency[:3]
    currency2 = currency[3:]
    return '為替レート (%s - %s)' % (currency1, currency2)
