import yfinance as yf
from matplotlib.figure import Figure


def clear_axes(fig: Figure):
    """
    チャートの消去
    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()


def draw_grid(fig: Figure):
    """
    チャートのグリッド
    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.grid(which='major', linestyle='solid')
        ax.grid(which='minor', linestyle='dotted')


def get_chart_title(ticker: yf.Ticker) -> str:
    """
    チャートのタイトル
    :param ticker:
    :return:
    """
    if 'longName' in ticker.info.keys():
        title = 'Daily chart for %s (%s)' % (ticker.info["longName"], ticker.ticker)
    elif 'shortName' in ticker.info.keys():
        title = 'Daily chart for %s (%s)' % (ticker.info["shortName"], ticker.ticker)
    else:
        title = 'Daily chart for %s' % ticker.ticker

    return title


def refresh_draw(fig: Figure):
    fig.canvas.draw()
