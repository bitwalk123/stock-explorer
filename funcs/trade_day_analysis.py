import pandas as pd
from matplotlib.patches import Rectangle

from widgets.charts import Trend


def draw_square(
        chart: Trend,
        df: pd.DataFrame,
        prange: float = 120
):
    rows = len(df)
    for r in range(rows - 1):
        idx1 = df.index[r]
        x1 = df['x'][idx1]
        y1 = df['y'][idx1]
        ptype1 = df['peak'][idx1]

        idx2 = df.index[r + 1]
        x2 = df['x'][idx2]
        y2 = df['y'][idx2]
        ptype2 = df['peak'][idx2]

        if abs(y1 - y2) > prange:
            if ptype1 == 'bottom':
                ecolor = '#004'
                fcolor = 'blue'
            else:
                ecolor = '#400'
                fcolor = 'red'
            chart.ax.add_patch(
                Rectangle((x1, y1), x2 - x1, y2 - y1,
                          edgecolor=ecolor,
                          facecolor=fcolor,
                          alpha=0.25,
                          fill=True,
                          lw=1,
                          joinstyle='round')
            )


def plot_peak(chart: Trend, df: pd.DataFrame, pcolor: str):
    chart.ax.plot(
        df['x'], df['y'],
        color=pcolor,
        marker='o',
        markersize=2,
        linewidth=0
    )


def check_peak(diff1, diff2, y):
    peak = list()
    for i in range(len(y)):
        d1 = diff1[i]
        d2 = diff2[i]
        if i == 0:
            if d2 < 0:
                peak.append('top')
            else:
                peak.append('bottom')
            continue

        if i == len(y) - 1:
            if d1 < 0:
                peak.append('bottom')
            else:
                peak.append('top')
            continue

        mul = d1 * d2
        if mul > 0:
            peak.append(None)
            continue
        elif mul == 0:
            if d2 == 0:
                if d1 == 0:
                    peak.append('None')
                elif d1 < 0:
                    peak.append('bottom')
                else:
                    peak.append('top')
            elif d2 > 0:
                peak.append('bottom')
            else:
                peak.append('top')
            continue

        if d1 < 0:
            peak.append('bottom')
        else:
            peak.append('top')
    return peak


def calc_diff(y):
    delta = list()
    for i in range(0, len(y) - 1):
        delta.append(y[i + 1] - y[i])
    return delta
