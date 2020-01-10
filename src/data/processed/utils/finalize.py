import pandas as pd
import json


def network_map(fp='json/networks.json'):
    with open(fp) as f:
        network_dict = json.load(f)

    name_dict = {}
    type_dict = {}
    for k in network_dict.keys():
        network_items = list(network_dict[k].items())
        for item in network_items:
            name_dict.update({int(item[0]):item[1]})
            type_dict.update({int(item[0]):k})

    return name_dict, type_dict


def restructure_columns(df):
    df = df.rename(columns={
        'season_number':'season',
        'episode_number':'episode',
        'vote_count':'votes',
        'vote_average':'rating',
        'ep_vote_count':'ep_votes',
        'ep_vote_average':'ep_rating'
        })

    cols = ['series_id',
            'series_name',
            'network_id',
            'network_name',
            'network_type',
            'genre_id',
            'genre_name',
            'status',
            'type',
            'origin_country',
            'original_language',
            'content_rating',
            'runtime',
            'popularity',
            'votes',
            'rating',
            'season',
            'episode',
            'air_date',
            'air_year',
            'ep_votes',
            'ep_rating']

    return df[cols]


def finalize(df):
    names, types = network_map()
    df['network_name'] = [names[k] for k in df['network_id']]
    df['network_type'] = [types[k] for k in df['network_id']]

    return restructure_columns(df)
