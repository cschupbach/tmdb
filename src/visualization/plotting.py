from utils import kde_contour as kd
import importlib
importlib.reload(kd)


def init_kde():
    years = [[2010,2011,2012],[2013,2014,2015],[2016,2017],[2018,2019]]
    labels = ['Cable','Streaming']
    cols = ['rating','votes']
    log = [False, True]

    return years, labels, cols, log


def get_contour_plots():
    years, labels, cols, log = init_kde()
    kd.contour_plots(years, labels, cols, log)

    return None


if __name__ == '__main__':
    get_contour_plots()
