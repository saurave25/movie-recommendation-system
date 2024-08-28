import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=05a406246d268107b249bd93b392d664&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie_title, movie_df, similarity):
    movie_index = movie_df[movie_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_posters = []

    recommend_movies = []
    for i in movie_list:
        movie_id = movie_df.iloc[i[0]].movie_id
        # fetch the posters from API

        recommend_movies.append(movie_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommended_movies_posters

# Load the movie data
movie_df = pickle.load(open('movie.pkl', 'rb'))
movie_list = movie_df['title'].values

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Select a movie:",
    movie_list
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie, movie_df, similarity)

    import streamlit as st

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])
