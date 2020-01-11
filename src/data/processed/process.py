import pandas as pd
import ast
from datetime import datetime as dt
from utils import parse
from utils import edit_tools as tools
from utils import networks
from utils import finalize


def process_series_data():
    df = pd.read_csv('../../../data/raw/series.csv')
    df['network_id'] = parse.dict_column(df['networks'], key='id')
    df['network_name'] = parse.dict_column(df['networks'], key='name')
    df['genre_id'] = parse.dict_column(df['genres'], key='id')
    df['genre_name'] = parse.dict_column(df['genres'], key='name')
    df['content_rating'] = parse.US_content_rating(df['content_ratings'])
    df['in_production'] = [int(s) for s in df['in_production']]
    df.loc[df.content_rating.isnull(), ['content_rating']] = 'NR'
    df = df.rename(columns={'id':'series_id','name':'series_name'})

    cols = ['series_id','series_name','first_air_date','last_air_date','in_production',
            'network_id','episode_run_time','origin_country','original_language','popularity',
            'status','type','vote_average','vote_count','content_rating','genre_id','genre_name']

    return df[cols]


def process_episode_data():
    series_data = process_series_data()
    data = pd.read_csv('../../../data/raw/episodes.csv')

    df = pd.concat([pd.DataFrame(ast.literal_eval(d)) for d in data['episodes']], sort=False)
    # df['air_date'] = pd.to_datetime(df['air_date'])
    df['air_year'] = pd.to_datetime(df['air_date']).dt.year
    df = df[(df.air_year>=2010)&(df.air_year<=2019)]
    df = df.rename(columns={'vote_average':'ep_vote_average','vote_count':'ep_vote_count','show_id':'series_id'})
    df = df.merge(series_data, on='series_id', how='left')

    df = tools.edit_network_ids(df)
    df = tools.edit_runtimes(df)
    df = tools.edit_origin_countries(df)
    df = tools.edit_first_air_dates(df)

    network_ids = [int(nwk) for nwk in networks.get_network_ids()]
    df = df[(df.runtime.notnull())&(df.network_id.isin(network_ids))]
    df.index = range(len(df))

    df = finalize.finalize(df)

    print('Writing: ../../../data/processed/data.csv')
    df.to_csv('../../../data/processed/data.csv', index=False)

    return None


if __name__ == '__main__':
    process_episode_data()
