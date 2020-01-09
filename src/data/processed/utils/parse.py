import ast
import numpy as np


def string_dict(string_dict, key):
    d = ast.literal_eval(string_dict)
    return [d[i][key] for i in range(len(d))]


def dict_column(col, key='id'):
    return [string_dict(s, key) for s in col]


def content_rating(string_dict):
    d = ast.literal_eval(string_dict)
    countries = [v[1] for v in [list(s.values()) for s in d['results']]]
    countries = [list(s.values()) for s in d['results']]
    try:
        idx = np.where(np.array(countries)[:,0]=='US')[0][0]
        return countries[idx][1]
    except IndexError:
        return np.nan


def US_content_rating(col):
    return [content_rating(s) for s in col]
