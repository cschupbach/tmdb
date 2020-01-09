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


def column_edits(df, col, fp):
    d = get_dictionary(fp)
    if type(list(d.values())[0]) == dict:
        for sid in d.keys():
            for szn in d[sid].keys():
                df.loc[(df.series_id==sid)&(df.season_number==szn), [col]] = d[sid][szn]
    else:
        for sid in d.keys():
            df.loc[(df.series_id==sid), [col]] = d[sid]

    return df


def origin_edits(df, col, fp):
    d = get_dictionary(fp)
    for sid in d.keys():
        for nwk in d[sid].keys():
            df.loc[(df.series_id==sid)&(df.network_id==nwk), [col]] = d[sid][nwk]

    return df


def edit_network_ids(df):
    df = df[(df.network_id.notnull())]
    df['network_id'] = [s[0] for s in df['network_id']]
    df = column_edits(df, col='network_id', fp='json/network_edits_01.json')
    df = column_edits(df, col='network_id', fp='json/network_edits_02.json')
    return df


def edit_runtimes(df):
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
    df = origin_edits(df, col='origin_country', fp='json/origin_country_edits.json')
    return df