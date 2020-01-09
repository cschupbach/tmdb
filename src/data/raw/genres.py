import pandas as pd
from utils import api
from utils import scraper


def get_genres():
    url = 'https://api.themoviedb.org'
    url += '/3/genre/tv/list?api_key={}&language=en-US'.format(api.get_key())
    data = scraper.get_data(url)

    df = pd.DataFrame(data['genres'])
    print('Writing: ../../../data/raw/genres.csv')
    df.to_csv('../../../data/raw/genres.csv', index=False)

    return None


if __name__ == '__main__':
    get_genres()
