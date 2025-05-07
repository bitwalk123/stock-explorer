import pandas as pd
from matplotlib.figure import Figure


def clearAxes(fig: Figure):
    """
    チャートの消去
    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()


def drawGrid(fig: Figure):
    """
    チャートのグリッド
    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.grid(which='major', linestyle='solid')
        ax.grid(which='minor', linestyle='dotted')


def refreshDraw(fig: Figure):
    fig.canvas.draw()
