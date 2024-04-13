import streamlit as st
import pandas as pd
import pickle
from imdb import Cinemagoer
import math

# create an instance of the Cinemagoer class
ia = Cinemagoer()

st.set_page_config(layout="wide")


def get_recommendations_general(name):
    movie_index = movies[movies['movie title'] == name].index
    movie_simularities = list(enumerate(simularity_general[movie_index].tolist()[0]))
    movie_simularities = sorted(movie_simularities, reverse=True, key=lambda x: x[1])
    movie_indexes = list(map(lambda x: x[0], movie_simularities[1:31]))
    return movies.iloc[movie_indexes][['movie title', 'imdb id', 'poster', 'rating', 'votes']]


def draw_recommendations(data):
    scrollable_bar_html = '<div style="overflow-x: auto; white-space: nowrap;">'
    for index in range(data.shape[0]):
        # st.write(movies["poster"][])
        scrollable_bar_html += f'<div style="display: inline-block; text-align: center; margin-right: 10px;">'
        scrollable_bar_html += f'<div style="margin-top: 5px; font-size: 24px;"><p id="text">{data.iloc[index, 0]}</p></div>'
        scrollable_bar_html += f'<img src="{data.iloc[index, 2]}" alt="Imageeee" style="width: 350px;">'
        scrollable_bar_html += f'<hr style="border: 1.3px solid white;">'
        scrollable_bar_html += f'<p class="littleBig red nl">Rating: </p><p class="littleBig nl">{data.iloc[index, 3]}</p>'
        scrollable_bar_html += f'<p></p>'
        scrollable_bar_html += f'<p class="littleBig red nl">Votes: </p><p class="littleBig nl">{data.iloc[index, 4]}</p>'
        scrollable_bar_html += '</div>'
    scrollable_bar_html += '</div>'

    # Display the HTML in the Streamlit app
    st.write(scrollable_bar_html, unsafe_allow_html=True)

st.title('TechFlix')
movies = pd.read_csv('Movies (1970-2023).csv')
simularity_general = pickle.load(open('simularities.pkl', 'rb'))
selection_layout, search_layout = st.columns([10, 1])

selected = selection_layout.selectbox(
    'Please Select a movie you would like to get recommendations for.',
    movies['movie title']
)

with open('style.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

submit = search_layout.button('Search')
if submit:
    draw_recommendations(get_recommendations_general(selected))