import pandas as pd
import ast
from datetime import datetime as dt
from utils import api
from utils import scraper


def get_series_seasons():
    series_data = pd.read_csv('../../../data/raw/series.csv')
    df = []
    for series_id, season in zip(series_data['id'], series_data['seasons']):
        szn = ast.literal_eval(season)
        for i in range(len(szn)):
            data = pd.DataFrame([szn[i]])
            data['id'] = series_id
            df.append(data)

    df = pd.concat(df, sort=False)
    df['air_date'] = pd.to_datetime(list(df['air_date']))
    df = df[(df.air_date.notnull())&(df.episode_count!=0)&(df.season_number!=0)]
    df['year'] = df['air_date'].dt.year
    df = df[df.year>=2009].drop_duplicates()

    return df['id'].values, df['season_number'].values


def _url(series_id, season):
    url = 'https://api.themoviedb.org/3/tv/{}/season/{}'.format(series_id, season)
    url += '?api_key={}&language=en-US'.format(api.get_key())
    return url


def get_episode_data():
    series_ids, seasons = get_series_seasons()
    dfs = []
    for i, szn in zip(series_ids, seasons):
        url = _url(i, szn)
        data = scraper.get_data(url)
        df = pd.DataFrame({k:[data[k]] for k in data.keys()})
        df['series_id'] = i
        dfs.append(df)
    dfs = pd.concat(dfs, sort=False)
    dfs.index = range(len(dfs))

    print('Writing: ../../../data/raw/episodes.csv')
    dfs.to_csv('../../../data/raw/episodes.csv', index=False)

    return None


if __name__ == '__main__':
    get_episode_data()
