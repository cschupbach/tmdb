import pandas as pd
import json
import ast

def integer_keys(d):
    if type(list(d.values())[0]) == dict:
        return {int(K):{int(k):v for k,v in d[K].items()} for K in d.keys()}
    else:
        return {int(k):v for k,v in d.items()}


def get_dictionary(fp):
    with open(fp) as f:
        return integer_keys(json.load(f))


def network_edits(df, col, fp):
    d = get_dictionary(fp)
    if type(list(d.values())[0]) == dict:
        for sid in d.keys():
            for szn in d[sid].keys():
                df.loc[(df.series_id==sid)&(df.season_number==szn), [col]] = d[sid][szn]
    else:
        for sid in d.keys():
            df.loc[(df.series_id==sid), [col]] = d[sid]

    return df


def column_edits(df, col, fp):
    d = get_dictionary(fp)
    for sid in d.keys():
        for nwk in d[sid].keys():
            df.loc[(df.series_id==sid)&(df.network_id==nwk), [col]] = d[sid][nwk]

    return df


def edit_network_ids(df):
    df = df[(df.network_id.notnull())].copy()
    df.loc[:,['network_id']] = [s[0] for s in df['network_id']]
    df = network_edits(df, col='network_id', fp='json/network_edits_01.json')
    df = network_edits(df, col='network_id', fp='json/network_edits_02.json')

    return df


def edit_runtimes(df):
    df.index = range(len(df))
    df['runtime'] = [ast.literal_eval(s) for s in df['episode_run_time']]
    df['runtime'] = pd.DataFrame(df['runtime'].tolist())[0]
    df = column_edits(df, col='runtime', fp='json/runtime_edits.json')

    return df.drop(['episode_run_time'], axis=1)


def edit_origin_countries(df):
    df.index = range(len(df))
    df['origin'] = [ast.literal_eval(s) for s in df['origin_country']]
    df = df.merge(pd.DataFrame(df['origin'].tolist()), left_index=True, right_index=True, how='left')
    df['n_origin'] = 5 - pd.DataFrame(df['origin'].tolist()).isna().sum(axis=1)
    df['origin_country'] = df.loc[:,[0,1,2,3,4,'n_origin']].fillna('').apply(lambda x: '/'.join(x[0:x['n_origin']]), axis=1)
    df = column_edits(df, col='origin_country', fp='json/origin_country_edits.json')

    return df



def edit_first_air_dates(df):
    d = {651:'1968-09-24', 91449:'2007-07-05', 6623:'1994-01-05', 65722:'2016-02-25'}
    for sid in d.keys():
        df.loc[(df.series_id==sid), ['first_air_date']] = d[sid]

    df = df[df.first_air_date.notnull()].copy()
    df.index = range(len(df))

    return df


def edit_genre_ids_names(df):
    df = network_edits(df, col='genre_name', fp='json/genre_name_edits.json')
    df = network_edits(df, col='genre_id', fp='json/genre_id_edits.json')
    df['genre_id'] = [str(s) for s in df['genre_id']]

    # Remove shows with missing genre or only genre is "News"
    df = df[~(df.genre_id.isin(['[]','[10763]']))].copy()
    # Remove talk shows
    df = df[df.type!='Talk Show'].copy()

    df.index = range(len(df))

    return df
