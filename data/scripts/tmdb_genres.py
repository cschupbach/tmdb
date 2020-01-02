import tmdb_scraper as tmdb
import pandas as pd


def get_genres(api_key):
    url = 'https://api.themoviedb.org'
    url += '/3/genre/tv/list?api_key={}&language=en-US'.format(api_key)
    data = tmdb.get_data(url)

    df = pd.DataFrame(data['genres'])
    print('Writing: ../raw/tv_genres.csv')
    df.to_csv('../raw/tv_genres.csv', index=False)

    return None
