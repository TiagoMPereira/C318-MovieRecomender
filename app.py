import streamlit as st
from model import MovieModel, InputPredict
import pandas as pd

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

    with st.form("my_form"):
        st.write("Movies Recommendation")

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
            runtime = st.slider("Duração", min_value=30, max_value=210, value=60)

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
            submitted = st.form_submit_button("Submit")

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
                            <li><b>Release Year:</b> {recommended.loc[recommended.index[i], "release_year"]}</li>
                            <li><b>Overview:</b> {recommended.loc[recommended.index[i], "overview"]}</li>
                            <li><b>Genres:</b> {recommended.loc[recommended.index[i], "genres"]}</li>
                            <li><b>Original Language:</b> {recommended.loc[recommended.index[i], "original_language"]}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True
                )

if __name__ == "__main__":
    run()
