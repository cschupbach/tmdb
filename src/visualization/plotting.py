from utils import kde_contour as kd
import importlib
importlib.reload(kd)


def init_kde():
    years = [[2010,2011,2012],[2013,2014,2015],[2016,2017],[2018,2019]]
    labels = ['Cable','Streaming']
    cols = ['popularity','votes']
    log = [True, True]

    return years, labels, cols, log


def get_contour_plots(save_fig=False):
    years, labels, cols, log = init_kde()
    kd.contour_plots(years, labels, cols, log, save_fig)

    return None


if __name__ == '__main__':
    get_contour_plots(save_fig=False)
