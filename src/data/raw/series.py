import numpy as np
import pandas as pd
from utils import api
from utils import scraper
from utils import networks


def id_url(pg, nw):
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=' + api.get_key()
    url += '&language=en-US&sort_by=vote_count.desc&air_date.gte=2010-01-01&with_networks={}&page={}'.format(nw, pg)
    return url


def get_series_id_list():
    network_ids = networks.get_network_ids()
    id_list = []
    for nw in network_ids:
        pg = 1
        total_pages = np.inf
        while pg <= total_pages:
            url = id_url(pg, nw)
            data = scraper.get_data(url)
            id_list += [d['id'] for d in data['results']]
            pg += 1
            total_pages = data['total_pages']

    return id_list


def series_url(series_id):
    url = 'https://api.themoviedb.org/3/tv/{}?api_key={}'.format(series_id, api.get_key())
    url += '&language=en-US&append_to_response=content_ratings'
    return url


def get_series_data():
    series_ids = get_series_id_list()
    df = []
    for series_id in series_ids:
        url = series_url(series_id)
        data = scraper.get_data(url)
        df.append(pd.DataFrame({k:[data[k]] for k in data.keys()}))
    df = pd.concat(df, sort=False)
    df.index = range(len(df))

    print('Writing: ../../../data/raw/series.csv')
    df.to_csv('../../../data/raw/series.csv', index=False)

    return None


if __name__ == '__main__':
    get_series_data()
