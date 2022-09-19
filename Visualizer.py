import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']


class Visualizer:
    """Initializes the plot that will be used to add lines to"""

    def __init__(self, title=None, xlabel='Timesteps', ylabel='Reward'):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if title is not None:
            self.ax.set_title(title)

    """Adds a line to the existing plot, based on data in y"""

    def add_curve(self, y, label=None, error=None):
        """ y: vector of average reward results
        label: string to appear as label in plot legend """
        indexes = np.where(np.isnan(y) | np.isinf(y))[0]
        if len(indexes):
            print('Ah-oh we\'ve got weird values here')
            move_positions = -1
            new_indexes = np.copy(indexes)
            for i in range(1, len(indexes)):
                if indexes[i] == indexes[i - 1] + 1:
                    # consecutive NA's or infinite's, so pick the real value left of it
                    new_indexes[i] = indexes[i + move_positions]
                    move_positions -= 1
                else:
                    # reset the offset
                    move_positions = -1

            y[indexes] = y[indexes - 1]
        if error is not None:
            error_data = np.apply_along_axis(np.std, 0, y, ddof=1) / np.sqrt(len(y))
            self.ax.errorbar(np.arange(y.shape[1]), smooth(np.apply_along_axis(np.mean, 0, y), window=3),
                             yerr=error_data, label=label)
            return
        if label is not None:
            self.ax.plot(y, label=label)
        else:
            self.ax.plot(y)

    """Plots the std on both sides of the mean of y"""

    def add_std(self, x, y_std, y_mean, alpha):
        self.ax.fill_between(x=x, y1=y_mean + y_std, y2=y_mean - y_std, alpha=alpha, facecolor='red')

    """Set bounds to y-axis"""

    def set_ylim(self, lower, upper):
        self.ax.set_ylim([lower, upper])

    """Plots a horizontal line on a set height"""

    def add_hline(self, height, label):
        self.ax.axhline(height, ls='--', c='k', label=label)

    """Saves the plot"""

    def save(self, name='test.png'):
        """ name: string for filename of saved figure """
        self.ax.legend(loc=2)
        self.fig.savefig(name, dpi=300)


"""Smoothes the curve using a savgol-filter"""


def smooth(y, window, poly=1):
    """
    y: vector to be smoothed
    window: size of the smoothing window """
    return savgol_filter(y, window, poly, mode='nearest')


def time_fetcher(file_name, label):
    data = np.load(file_name)
    data = data[data[:, 0].argsort()]

    data_per_query = np.split(data[:, 1], np.unique(data[:, 0], return_index=True)[1][1:])
    query_times_mean, query_times_std = [], []
    for i in range(len(data_per_query)):
        query_times_mean.append(np.mean(data_per_query[i]))
        query_times_std.append(np.std(data_per_query[i]))
    return query_times_mean, query_times_std, label


def dual_bar_plot(title, data_for_bars, x_axis, y_axis, legend, save_location):
    ind = np.arange(len(data_for_bars[0][0]))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, data_for_bars[0][0], width, yerr=data_for_bars[0][1],
                    label=data_for_bars[0][2])
    rects2 = ax.bar(ind + width / 2, data_for_bars[1][0], width, yerr=data_for_bars[1][1],
                    label=data_for_bars[1][2])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels([str(i + 1) for i in ind])
    if legend:
        ax.legend()

    fig.tight_layout()

    plt.savefig(save_location) # save it in higher res when using it in the report
    plt.show()


if __name__ == '__main__':
    dual_bar_plot('Runtime differences between MonetDB and MySQL',
             [time_fetcher('results/binary_results/Job_Desktop_MonetDB_SF-1.npy', 'MonetDB'),
              time_fetcher('results/binary_results/Job_Desktop_MySQL_SF-1.npy', 'MySQL')],
             'Query',
             'Time (s)',
             True,
             'results/plot.png')
