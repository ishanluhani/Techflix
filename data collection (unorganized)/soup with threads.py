import time
import pickle
import imdb
import concurrent.futures
from collections import deque
import numpy as np
import pandas as pd


def get_movie_info(movie_title):
    ia = imdb.IMDb()
    movies = ia.search_movie(movie_title)

    if not movies:
        print(f"No movie found with the title: {movie_title}")
        return

    movie = ia.get_movie(movies[0].getID())
    imdb_id = movie.movieID
    cast = [actor['name'] for actor in movie['cast']]
    plot = movie.get('plot', [])
    if not plot:
        plot = movie.get('plot outline', pd.NA)
    if isinstance(plot, list):
        plot = plot[0]
    director = movie.get('directors', '')
    if not director:
        director = movie.get('director', pd.NA)
    if isinstance(director, list):
        director = director[0]
    rating = movie.get('rating', pd.NA)
    votes = movie.get('votes', pd.NA)
    year = movie.get('year', pd.NA)
    runtime = movie.get('runtimes', pd.NA)
    genres = movie.get('genres', pd.NA)
    poster = movie.get('full-size cover url', pd.NA)
    languages = movie.get('languages', pd.NA)
    title = movie['title']
    print(movie.items())

    return title, imdb_id, cast, plot, director, rating, genres, poster, votes, year, runtime, languages

def process_movie(movie_title, n=7):
    global count, movie_data
    movie_title, language_cinema = movie_title
    try:
        title, imdb_id, cast, plot, director, rating, genres, poster, votes, year, runtime, languages = get_movie_info(movie_title)
        count += 1
        print(count)
        movie_data.append(np.array([str(title), str(imdb_id), str(cast), str(plot), str(director), str(rating), str(genres), str(poster), str(language_cinema), str(votes), str(year), str(runtime), str(languages)]))
        print(f"Title: {movie_title}, IMDb ID: {imdb_id}, Cast: {', '.join(cast)}, Plot: {plot}, Director: {director}")
    except Exception as e:
        print(f"Error processing {movie_title}: {e}")
        if n == 0:
            pass
        else:
            time.sleep(4)
            process_movie(movie_title, language_cinema, n-1)


movie_data = deque()
for years in range(1970, 2024):
    for i in ['Hindi', 'American']:
        if years != 2017:
            datas_link = pd.read_html(f'https://en.wikipedia.org/wiki/List_of_{i}_films_of_{years}')
            datas = []
            for data in datas_link:
                if 'Title' in data.columns or 'Film' in data.columns:
                    datas.append(data)
            try:
                final = pd.concat(datas)['Title']
            except KeyError:
                final = pd.concat(datas)['Film']
            print('----------------------------------------------------------------------')
            count = 0
            final.dropna(inplace=True)
            print(len(final))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(process_movie, zip(final, [i]*len(final)))
            final = pd.Series()
    pickle.dump(movie_data, open('movies_data.pkl', 'wb'))

for years in range(2010, 2024):
    for i in ['Telugu', 'Tamil', 'Kannada', 'Marathi']:
        if years != 2017:
            datas_link = pd.read_html(f'https://en.wikipedia.org/wiki/List_of_{i}_films_of_{years}')
            datas = []
            for data in datas_link:
                if 'Title' in data.columns or 'Film' in data.columns:
                    datas.append(data)
            try:
                final = pd.concat(datas)['Title']
            except KeyError:
                final = pd.concat(datas)['Film']
            print('----------------------------------------------------------------------')
            count = 0
            final.dropna(inplace=True)
            print(len(final))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(process_movie, zip(final, [i]*len(final)))
            final = pd.Series()
    pickle.dump(movie_data, open('movies_data.pkl', 'wb'))

print(len(movie_data))
print(movie_data)
pickle.dump(movie_data, open('movies_data.pkl', 'wb'))