import tmdb_scraper as tmdb
import pandas as pd
import numpy as np
from datetime import datetime as dt


def _url(api_key, page, min_votes):
    url = 'https://api.themoviedb.org'
    url += '/3/discover/tv?api_key={}&sort_by=vote_count.desc'.format(api_key)
    url += '&vote_count.gte={}&language=en-US&page={}'.format(str(min_votes), str(page))
    return url


def get_series_data(api_key, page=1, min_votes=0):
    total_pages = np.inf
    all_data = []
    while page <= total_pages:
        url = _url(api_key, page, min_votes)
        data = tmdb.get_data(url)
        all_data += data['results']

        total_pages = data['total_pages']
        page += 1

    df = pd.DataFrame(all_data)
    df['access_date'] = dt.now()

    print('Writing: ../raw/tv_series.csv')
    df.to_csv('../raw/tv_series.csv', index=False)

    return None
