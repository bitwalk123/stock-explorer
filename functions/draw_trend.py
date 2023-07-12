from functions.get_open_with_code import get_open_with_code
from ui_modules.charts import Trend


def draw_trend(chart: Trend, code: int):
    """Draw chart with specified ticker code

    Args:
        chart (Trend): instance of Trend
        code (int): ticker code
    """
    cname, list_x, list_y = get_open_with_code(code)
    chart.clearAxes()
    #
    chart.axes.plot(list_x, list_y)
    chart.axes.set_title('%s (%d.T)' % (cname, code))
    chart.axes.set_xlabel('日付')
    chart.axes.set_ylabel('株価')
    chart.axes.grid()
    #
    chart.refreshDraw()
