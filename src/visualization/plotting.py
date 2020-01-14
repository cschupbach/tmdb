from utils import kde_contour as kd
import importlib
importlib.reload(kd)


def init_kde(plot_number):
    years = {
        0:[[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]],
        1:[[2010,2011,2012,2013],[2014,2015],[2016,2017],[2018,2019]],
        2:[[2010,2011,2012,2013],[2014,2015],[2016,2017],[2018,2019]],
        3:[[2010,2011,2012,2013],[2014,2015],[2016,2017],[2018,2019]],
        4:[[2010,2011,2012,2013],[2014,2015],[2016,2017],[2018,2019]]
    }
    labels = {
        0:['Cable','Streaming'],
        1:['Cable','Streaming'],
        2:['Cable','Streaming'],
        3:['Cable','Premium'],
        4:['Streaming','Premium']
    }
    cols = ['rating','votes']
    log = [False, True]

    return years[plot_number], labels[plot_number], cols, log


def get_contour_plots(plot_number, save_fig):
    compare = (i!=0 and i!=1)
    years, labels, cols, log = init_kde(plot_number)
    kd.contour_plots(years, labels, cols, log, save_fig, compare)

    return None


if __name__ == '__main__':
    for i in range(5):
        get_contour_plots(i, save_fig=False)
