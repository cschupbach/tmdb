import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import os
import matplotlib.pyplot as plt


def get_data(fp='../../data/processed/data.csv', cols=['rating','votes'], log=[False,False]):
    df = pd.read_csv(fp)
    df = df[df.votes>0].sort_values(by='air_date', ascending=False).drop_duplicates(['series_id'])
    df['release_year'] = pd.to_datetime(df['release']).dt.year
    for i,j in zip(cols, log):
        if j == True:
            df[i] = np.log(df[i])

    return df


def get_extent(X):
    xmin = X[:,0].min()
    xmax = X[:,0].max()
    ymin = X[:,1].min()
    ymax = X[:,1].max()

    return xmin, xmax, ymin, ymax


def create_meshgrid(X, gridsize=500j):
    xmin, xmax, ymin, ymax = get_extent(X)
    extent = [xmin, xmax, ymin, ymax]
    xx, yy = np.mgrid[xmin:xmax:gridsize, ymin:ymax:gridsize]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    return xx, yy, positions, extent


def format_axes(ax, extent, features, years, log):
    ax.set_xlim(extent[:2])
    ax.set_ylim(extent[2:])
    if log[0] == True:
        ax.set_xlabel('log({})'.format(features[0]), size=12)
    else:
        ax.set_xlabel(features[0], size=12)
    if log[1] == True:
        ax.set_ylabel('log({})'.format(features[1]), size=12)
    else:
        ax.set_ylabel(features[1], size=12)
    if len(years) > 1:
        ax.set_title('{} - {}'.format(years[0], years[-1]), size=13)
    else:
        ax.set_title('{}'.format(years[0]), size=13)

    return ax


def kernelize(X, xx, positions):
    values = np.vstack([X[:,0], X[:,1]])
    kernel = sp.stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, xx.shape)

    return Z


def plot_params():
    cmap = [plt.cm.PuBu, plt.cm.PuRd]
    c = ['navy', 'red']
    alpha = [1.0, 0.6]

    return cmap, c, alpha


def max_density(Z, xx, yy):
    max_xx = xx[np.where(Z==np.max(Z))[0][0],:][0]
    max_yy = yy[:,np.where(Z.T==np.max(Z))[0][0]][0]
    return [max_xx, max_yy]


def KDE_stats(Z, xx, yy, X, years, log):
    samples = len(X[:,0])/len(years)
    xy_est = max_density(Z, xx, yy)
    kstats = [samples]
    for i in range(2):
        if log[i] == True:
            kstats += [np.exp(xy_est[i])]
        else:
            kstats += [xy_est[i]]

    return kstats


def fig_title(fig, cols, labels, compare):
    if compare == True:
        fig.suptitle('KDE contour plots comparing the number of votes and {}\n'.format(cols[0]) +\
            'of {} and {} TV shows throughout the 2010s'.format(labels[0], labels[1]), size=16)
    else:
        fig.suptitle('KDE contour plots comparing the number of votes and {}\n'.format(cols[0]) +\
            'of TV shows throughout the 2010s', size=16)

    return None


def plot_text(ax, i, extent, label, features, c, kstats, compare):
    xloc = extent[0] + 0.5
    yloc = [extent[3]-0.7, extent[3]-2.2]
    if compare == True:
        ax.text(xloc, yloc[i], label, size=12, bbox=dict(facecolor=c, alpha=0.3))
    ax.text(xloc, yloc[i]-0.4, 'N (per year): {:.1f}'.format(kstats[0]), size=10)
    ax.text(xloc, yloc[i]-0.7, 'KDE {}: {:.1f}'.format(features[0], kstats[1]), size=10)
    ax.text(xloc, yloc[i]-1.0, 'KDE {}: {:.1f}'.format(features[1], kstats[2]), size=10)

    return ax


def png_number():
    name = str(len([f for f in os.listdir('../../figures/') if 'kde_contour' in f])+1)
    if len(name) == 1:
        return '0' + name
    else:
        return name


def compare_kde_contours(df, ax, X, years, features, labels, log, compare):
    sns.set_style('white')

    X0 = df[features].to_numpy()
    xx, yy, positions, extent = create_meshgrid(X0, gridsize=200j)
    cmap, c, alpha = plot_params()

    if compare == True:
        X = X[1:]
    else:
        X = X[:1]
    ax = format_axes(ax, extent, features, years, log)
    kstats_dict = {}
    for i in range(len(X)):
        Z = kernelize(X[i], xx, positions)
        kstats = KDE_stats(Z, xx, yy, X[i], years, log)
        kstats_dict.update({np.mean(years):kstats})
        ax = plot_text(ax, i, extent, labels[i], features, c[i], kstats, compare)
        ax.imshow(np.rot90(Z), cmap=cmap[i], extent=extent, alpha=alpha[i])
        ax.contour(xx, yy, Z, colors=c[i], levels=10, linewidths=0.5, alpha=0.7)
        ax.scatter(X[i][:,0], X[i][:,1], c=c[i], s=5, alpha=alpha[i]/5)

    return kstats_dict


def figure_layout(years):
    if len(years) == 1:
        ncols = 1
    else:
        ncols = 2
    nrows = np.ceil(len(years)/ncols)
    width = ncols*8
    height = np.ceil(((nrows-1)*6)+7.5)

    return ncols, nrows, width, height


def contour_plots(years, labels, cols, log, save_fig, compare):
    df = get_data(cols=cols, log=log)
    ncols, nrows, width, height = figure_layout(years)
    fig = plt.figure(figsize=(width, height))
    ax = [plt.subplot(nrows, ncols, i+1) for i in range(len(years))]
    fig_title(fig, cols, labels, compare)
    kstats_dict = {}
    for i in range(len(years)):
        X0 = df[(df.release_year.isin(years[i]))][cols].to_numpy()
        X1 = df[(df.network_type==labels[0])&(df.release_year.isin(years[i]))][cols].to_numpy()
        X2 = df[(df.network_type==labels[1])&(df.release_year.isin(years[i]))][cols].to_numpy()
        X = [X0,X1,X2]
        kstats_dict.update(compare_kde_contours(df, ax[i], X, years[i], cols, labels, log, compare))

    if save_fig == True:
        fig.savefig('../../figures/kde_contour_{}.png'.format(png_number()))

    return kstats_dict
