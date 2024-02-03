import streamlit as st
from sections import navbar
from functions.utility import get_data
from icecream import ic


def run():
    st.query_params.page = "start_or_join_game"
    navbar.run()
    st.write("Start new game")
    st.write(st.session_state)

    start_new_game, join_game = st.tabs(["Start New Game", "Join with Game Code"])

    with start_new_game:
        st.header("Start New Game")
        characters = get_data("characters").keys()
        st.radio("Choose Your Character", options=characters, key="start_as_character")
        if st.button("Begin the Quest"):
            st.query_params.page = "play"
            st.query_params.game = "123"
            st.query_params.player = "abc"
            st.rerun()

    with join_game:
        st.header("Join with Game Code")
        code_column, unused = st.columns([2, 10])
        with code_column:
            game_code = st.text_input("Enter Game Code")

            if game_code:
                characters = get_data("characters").keys()
                st.radio(
                    "Choose Your Character", options=characters, key="join_as_character"
                )
                if st.button("Join the Quest"):
                    st.query_params.page = "play"
                    st.query_params.game = "123"
                    st.query_params.player = "abc"
                    st.rerun()
