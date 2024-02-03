import streamlit as st
from sections import navbar
from functions.utility import get_data
from icecream import ic
import coolname


@st.cache_data(ttl=600)
def get_code_options(type: str = None):
    codes = coolname.generate()
    codes = [code for code in codes if len(code) > 2]
    return codes


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
        st.write("Share the Game Code with your fellow players so they can join")
        game_code = st.radio("Choose Game Code", options=get_code_options("game"))
        st.write(
            "Use the Player Code to resume the game as your character if you reload the site"
        )
        player_code = (
            st.radio(
                "Choose Player Code",
                options=get_code_options("start_player"),
                key="start_player_code",
            ),
        )

        if st.button("Begin the Quest"):
            st.query_params.page = "play"
            st.query_params.game = game_code
            st.query_params.player = player_code
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
                st.write(
                    "Use the Player Code to resume the game as your character if you reload the site"
                )
                player_code = st.radio(
                    "Choose Player Code",
                    options=get_code_options("join_player"),
                    key="join_player_code",
                )
                if st.button("Join the Quest"):
                    st.query_params.page = "play"
                    st.query_params.game = game_code
                    st.query_params.player = player_code
                    st.rerun()
