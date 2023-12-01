import streamlit as st
from model import MovieModel, InputPredict
import pandas as pd
import numpy as np
from copy import copy
import seaborn as sns
import matplotlib.pyplot as plt

def run():

    model = MovieModel.load("movie_model_fitted.mr")

    genres = [
        'action', 'adventure', 'animation', 'comedy', 'crime',
        'documentary', 'drama', 'family', 'fantasy', 'foreign',
        'history', 'horror', 'music', 'mystery', 'romance',
        'science_fiction', 'thriller', 'war', 'western'
    ]

    languages = [
        'chinese', 'english', 'french', 'german', 'hindi',
        'italian', 'japanese', 'korean', 'portuguese', 'russian', 'spanish'
    ]

    recommended = None  # Initialize recommended outside the if block
    user_input = None

    with st.form("my_form"):
        st.write("Recomendador de filmes")

        # Create three columns for the select boxes
        col1, col2, col3 = st.columns(3)

        # Place the select boxes in separate columns
        with col1:
            genre1 = st.selectbox("Gênero - 1", genres, index=None, placeholder="Qual gênero você deseja?")

        with col2:
            genre2 = st.selectbox("Gênero - 2", genres, index=None, placeholder="Qual gênero você deseja?")

        with col3:
            genre3 = st.selectbox("Gênero - 3", genres, index=None, placeholder="Qual gênero você deseja?")

        # Create two columns for the sliders
        col4, col5 = st.columns(2)

        with col4:
            runtime = st.slider("Duração (min)", min_value=30, max_value=210, value=60)

        with col5:
            release = st.slider("Ano de lançamento", min_value=1906, max_value=2017, value=1990)

        # Create three columns for the language and submit button
        col7, col8 = st.columns(2)

        with col7:
            language = st.selectbox("Idioma", languages, index=None, placeholder="Qual idioma original?")

        with col8:
            st.text("")  # Placeholder for centering
            st.text("")  # Placeholder for centering
            # Place the submit button
            submitted = st.form_submit_button("Recomendar")

            # Initialize recommended inside the if block
            if submitted:
                user_input = InputPredict()
                user_input.genre1 = genre1
                user_input.genre2 = genre2
                user_input.genre3 = genre3
                user_input.release_year = release
                user_input.runtime = runtime
                user_input.language = language

                recommended = model.predict(user_input)

    # Create a separate frame for the result
    result_frame = st.container()

    # Display the result inside the frame with a border
    with result_frame:
        if recommended is not None:
            for i in range(len(recommended)):
                st.markdown(
                    f"""
                    <div style="border: 2px solid #e1e1e1; padding: 10px; border-radius: 5px; margin-top: 20px;">
                        <h3>{i + 1}: {recommended.loc[recommended.index[i], "title"]}</h3>
                        <ul>
                            <li><b>Ano de lançamento:</b> {recommended.loc[recommended.index[i], "release_year"]}</li>
                            <li><b>Resumo:</b> {recommended.loc[recommended.index[i], "overview"]}</li>
                            <li><b>Gêneros:</b> {recommended.loc[recommended.index[i], "genres"]}</li>
                            <li><b>Idioma original:</b> {recommended.loc[recommended.index[i], "original_language"]}</li>
                            <li><b>Duração (min):</b> {recommended.loc[recommended.index[i], "runtime"]}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True
                )

    # Create Importance section
    importance_frame = st.container()

    with importance_frame:
        if user_input:
            st.markdown(
                    f"""
                    <br><br>
                    """, unsafe_allow_html=True
                )
            importance = get_importance(model, user_input)
            st.write("Importância das variáveis (Quanto menor, maior o impacto)")
            plot_heatmap(pd.DataFrame(importance).T)

def plot_heatmap(df):
    fig, ax = plt.subplots()
    sns.heatmap(df, annot=True, cmap=plt.cm.Blues, fmt='.2f', ax=ax)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(df.columns, rotation = 50)
    st.pyplot(fig)

def get_importance(model: MovieModel, input_: InputPredict):
        recommended = model.predict(input_)
        main_movies = recommended.head(5)

        main_indexes = main_movies.index

        movies_explainability = {}

        for movie_id in main_indexes:
            movie_name = recommended.loc[recommended.index == movie_id, "title"].values[0]

            explanation = {}
            default_score = recommended.loc[recommended.index == movie_id, "probability"].values[0]
            movie_input = copy(input_)

            # Genre 1
            movie_input.genre1 = None
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["genre1"] = round(score, 3)
            movie_input.genre1 = input_.genre1

            # Genre 2
            movie_input.genre2 = None
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["genre2"] = round(score, 3)
            movie_input.genre2 = input_.genre2

            # Genre 3
            movie_input.genre3 = None
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["genre3"] = round(score, 3)
            movie_input.genre3 = input_.genre3

            # Release year
            movie_input.release_year = 0
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["release_year"] = round(score, 3)
            movie_input.release_year = input_.release_year

            # Runtime
            movie_input.runtime = 0
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["runtime"] = round(score, 3)
            movie_input.runtime = input_.runtime

            # Language
            movie_input.language = None
            pred = model.predict(movie_input, n_predictions=50000)
            score = np.abs(default_score - pred.loc[pred.index == movie_id, "probability"].values[0])

            explanation["language"] = round(score, 3)
            movie_input.language = input_.language

            movies_explainability[movie_name] = explanation

        return movies_explainability

if __name__ == "__main__":
    run()
