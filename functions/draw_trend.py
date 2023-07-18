from functions.get_open_with_code import get_open_with_code
from ui_modules.charts import Trend


def draw_trend(chart: Trend, code: int = 0):
    """Draw chart with specified ticker code

    Args:
        chart (Trend): instance of Trend
        code (int): ticker code
    """
    if code > 0:
        cname, list_x, list_y = get_open_with_code(code)
    else:
        cname = None
        list_x = list()
        list_y = list()
    chart.clearAxes()
    #
    chart.axes.plot(list_x, list_y)
    if code > 0:
        chart.axes.set_title('%s (%d.T)' % (cname, code))
    chart.axes.set_xlabel('DATE')
    chart.axes.set_ylabel('PRICE')
    chart.axes.grid()
    #
    chart.refreshDraw()
