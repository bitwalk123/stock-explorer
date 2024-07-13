import numpy as np

from matplotlib.axes import Axes

from structs.dta import DTAObj
from widgets.charts import ChartForAnalysis, yaxis_fraction


class DTAPlotBase():
    def __init__(self, chart: ChartForAnalysis, dtaobj: DTAObj):
        self.chart = chart
        self.dtaobj = dtaobj
        self.init_chart()

    def draw(self):
        # Data disctionary
        dict_data = self.dtaobj.getPlotData(0, robust=False)
        # _____________________________________________________________________
        # Scaled
        self.chart.ax1.scatter(
            dict_data['x'],
            dict_data['y_scaled'],
            s=1,
            c='#444'
        )
        stock_ticker = self.dtaobj.getTicker()
        date_str = self.dtaobj.getDateStr()
        legend_str = '%s : %s' % (stock_ticker, date_str)
        # _____________________________________________________________________
        # Smoothing Spline
        self.chart.ax1.fill_between(
            dict_data['xs'],
            dict_data['ys'],
            alpha=0.1
        )
        self.chart.ax1.plot(
            dict_data['xs'],
            dict_data['ys'],
            lw=1,
            label=legend_str
        )
        self.chart.ax1.xaxis.set_ticks(np.arange(0, 18000, 1800))
        self.chart.ax1.set_xlim(0, 18000)
        self.chart.ax1.set_ylim(self.get_ylim(self.dtaobj))
        self.chart.ax1.legend(loc='best')

        # _____________________________________________________________________
        # 1st Derivatives
        self.chart.ax2.plot(
            dict_data['xs'],
            dict_data['dy1s'],
            lw=1
        )
        yaxis_fraction(self.chart.ax2)

        # _____________________________________________________________________
        # 2nd Derivatives
        self.chart.ax3.plot(
            dict_data['xs'],
            dict_data['dy2s'],
            lw=1
        )
        yaxis_fraction(self.chart.ax3)
        # refresh
        self.chart.refreshDraw()

    def init_chart(self):
        self.chart.clearAxes()
        for ax in self.chart.fig.axes:
            self.set_hvlines(ax)
            ax.grid()
        # _____________________________________________________________________
        # X axis label
        self.chart.ax3.set_xlabel('Tokyo Market Opening [sec]')
        # _____________________________________________________________________
        # Y axes label
        self.chart.ax1.set_ylabel('Standardized Price')
        self.chart.ax2.set_ylabel('$dy$')
        self.chart.ax3.set_ylabel('$dy^2$')

    @staticmethod
    def get_ylim(dtaobj: DTAObj) -> tuple[float, float]:
        y_min = dtaobj.getYMin()
        y_max = dtaobj.getYMax()
        y_pad = (y_max - y_min) * 0.05

        ylim_min = y_min - y_pad
        ylim_max = y_max + y_pad

        return ylim_min, ylim_max

    @staticmethod
    def set_hvlines(ax: Axes):
        ax.axhline(y=0, linestyle='solid', lw=0.75, c='black')
        ax.axvline(x=9000, linestyle='dotted', lw=1, c='red')
        ax.axvline(x=18000, linestyle='dotted', lw=1, c='gray')


class DTAPlotSim(DTAPlotBase):
    def __init__(self, chart: ChartForAnalysis, dtaobj: DTAObj):
        super().__init__(chart, dtaobj)
        self.list_y = None
        self.list_x = None
        self.size_max = None
        self.counter = None
        self.dict_data = None

    def draw(self):
        # Data disctionary
        self.dict_data = self.dtaobj.getPlotData(0, robust=False)
        self.counter = 0
        self.size_max = len(self.dict_data['x'])
        # print('size max', self.size_max)

        self.list_x = list()
        self.list_y = list()

    def update_data(self):
        x = self.dict_data['x'][self.counter]
        y = self.dict_data['y_scaled'][self.counter]
        self.list_x.append(x)
        self.list_y.append(y)

        self.init_chart()
        self.chart.ax1.scatter(self.list_x, self.list_y, s=1, c='#444')
        # refresh
        self.chart.refreshDraw()

        self.counter += 1

    def shouldStopTimer(self):
        if self.counter >= self.size_max:
            return True
        else:
            return False
