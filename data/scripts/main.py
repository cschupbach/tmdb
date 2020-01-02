import sys
import tmdb_genres as genres
import tmdb_tv_series as tv

api_key = sys.argv[1]

if __name__ == '__main__':
    genres.get_genres(api_key)
    tv.get_series_data(api_key)
