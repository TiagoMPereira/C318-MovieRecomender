import streamlit as st
from model import MovieModel, InputPredict
import pandas as pd

def run():

    model = MovieModel.load("movie_model_fitted.mr")

    genres = [
        'action',
        'adventure',
        'animation',
        'comedy',
        'crime',
        'documentary',
        'drama',
        'family',
        'fantasy',
        'foreign',
        'history',
        'horror',
        'music',
        'mystery',
        'romance',
        'science_fiction',
        'thriller',
        'war',
        'western'
    ]
    languages = [
        'chinese',
        'english',
        'french',
        'german',
        'hindi',
        'italian',
        'japanese',
        'korean',
        'portuguese',
        'russian',
        'spanish'
    ]

    with st.form("my_form"):
        st.write("Movies Recommendation")
        genre1 = st.selectbox("Gênero - 1", genres, index=None, placeholder="Qual gênero você deseja?")
        genre2 = st.selectbox("Gênero - 2", genres, index=None, placeholder="Qual gênero você deseja?")
        genre3 = st.selectbox("Gênero - 3", genres, index=None, placeholder="Qual gênero você deseja?")
        runtime = st.slider("Duração", min_value=30, max_value=210, value=60)
        release = st.slider("Ano de lançamento", min_value=1906, max_value=2017, value=1990)
        language = st.selectbox("Idioma", languages, index=None, placeholder="Qual idioma orignal?")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            # st.write("Duração", runtime)
            # st.write("Gênero 1", genre1)
            # st.write("Gênero 2", genre2)
            # st.write("Gênero 3", genre3)
            # st.write("Ano de lançamento", release)
            # st.write("Idioma", language)

            user_input = InputPredict()
            user_input.genre1 = genre1
            user_input.genre2 = genre2
            user_input.genre3 = genre3
            user_input.release_year = release
            user_input.runtime = runtime
            user_input.language = language

            recommended = model.predict(user_input)

            st.write("1:", recommended.loc[recommended.index[0],"title"])
            st.write("2:", recommended.loc[recommended.index[1],"title"])
            st.write("3:", recommended.loc[recommended.index[2],"title"])
            st.write("4:", recommended.loc[recommended.index[3],"title"])
            st.write("5:", recommended.loc[recommended.index[4],"title"])
            

    st.write("Outside the form")

if __name__ == "__main__":
    run()